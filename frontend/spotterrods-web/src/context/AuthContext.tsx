import { toast } from "sonner";
import { api } from "@/lib/axios";
import axios, { AxiosRequestConfig, AxiosResponse } from "axios";
import {
  createContext,
  useContext,
  useState,
  useEffect,
  useCallback,
  useRef,
  useMemo,
} from "react";

interface LoginResponseProps {
  accessToken: string;
  refreshToken: string;
}

interface UserProps {
  id: string;
  username: string;
  name: string;
  role: string;
}

interface AuthContextProps {
  user: UserProps | null;
  login: (username: string, password: string) => Promise<void>;
  logout: () => void;
  loading: boolean;
}

const storage = {
  get: (key: string) => localStorage.getItem(key),
  set: (key: string, value: string) => localStorage.setItem(key, value),
  remove: (key: string) => localStorage.removeItem(key),
};

const AuthContext = createContext<AuthContextProps | undefined>(undefined);

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
  const [user, setUser] = useState<UserProps | null>(null);
  const [accessToken, setAccessToken] = useState<string | null>(null);
  const [refreshToken, setRefreshToken] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const isRefreshing = useRef(false);
  const failedQueue: Array<{
    resolve: (token: string) => void;
    reject: (error: any) => void;
  }> = useMemo(() => [], []);

  const processQueue = useCallback(
    (error: any, token: string | null = null) => {
      failedQueue.forEach((promise) => {
        if (token) {
          promise.resolve(token);
        } else {
          promise.reject(error);
        }
      });

      failedQueue.length = 0;
    },
    [failedQueue]
  );

  useEffect(() => {
    const interceptorId = api.interceptors.request.use((config) => {
      if (accessToken) {
        config.headers.Authorization = `Bearer ${accessToken}`;
      }
      config.withCredentials = true;
      return config;
    });

    const responseInterceptor = api.interceptors.response.use(
      (response: AxiosResponse) => response,
      async (error: any) => {
        const originalRequest: AxiosRequestConfig & { _retry?: boolean } =
          error.config;

        if (error.response?.status === 401 && !originalRequest._retry) {
          if (isRefreshing.current) {
            return new Promise((resolve, reject) => {
              failedQueue.push({ resolve, reject });
            })
              .then((token: unknown) => {
                originalRequest.headers = originalRequest.headers || {};
                originalRequest.headers.Authorization = `Bearer ${token}`;
                return api.request(originalRequest);
              })
              .catch((err) => Promise.reject(err));
          }

          originalRequest._retry = true;
          isRefreshing.current = true;

          try {
            console.log("Token expired, refreshing");
            const { data } = await api.post(
              "/auth/refresh/",
              {refreshToken},
              {
                withCredentials: true,
              }
            );

            const { accessToken: newAccessToken } = data;

            setAccessToken(newAccessToken);
            storage.set("access_token", newAccessToken);

            processQueue(null, newAccessToken);

            originalRequest.headers = originalRequest.headers || {};
            originalRequest.headers.Authorization = `Bearer ${newAccessToken}`;

            return api.request(originalRequest);
          } catch (refreshError) {
            console.error("Failed to refresh token: ", refreshError);
            processQueue(refreshError, null);
            logout();
          } finally {
            isRefreshing.current = false;
          }
        }

        return Promise.reject(error);
      }
    );

    return () => {
      api.interceptors.request.eject(interceptorId);
      api.interceptors.request.eject(responseInterceptor);
    };
  }, [accessToken, failedQueue, processQueue]);

  const fetchUserProfile = useCallback(async (token: string) => {
    try {
      const { data } = await api.get("/auth/profile", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      setUser(data);
    } catch (error) {
      console.error("Failed to fetch user profile: ", error);
      logout();
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    setLoading(true);
    const storedAccessToken = storage.get("access_token");
    const storedRefreshToken = storage.get("refresh_token");

    if (storedAccessToken && storedRefreshToken) {
      setAccessToken(storedAccessToken);
      setRefreshToken(storedRefreshToken);
      fetchUserProfile(storedAccessToken);
    } else {
      setLoading(false);
    }
  }, [fetchUserProfile]);

  const login = async (username: string, password: string) => {
    try {
      setLoading(true);
      const { data }: { data: LoginResponseProps } = await api.post(
        "/auth/login/",
        { username, password },
        { withCredentials: true }
      );
      
      console.log(data);

      const { accessToken, refreshToken } = data;
      setAccessToken(accessToken);
      setRefreshToken(refreshToken);

      storage.set("access_token", accessToken);
      storage.set("refresh_token", refreshToken);

      await fetchUserProfile(accessToken);

      setLoading(false);
      toast("Logged in successfully");
    } catch (error) {
      setLoading(false);
      if (axios.isAxiosError(error)) {
        toast(`${error.response?.data || error.message}`);
        console.error("Login Failed: ", error.response?.data || error.message);
      } else {
        toast(`${(error as Error).message || "Unknown error occurred"}`);
        console.log(
          "Login Failed: ",
          (error as Error).message || "Unknown error occurred"
        );
      }
    }
  };

  const logout = () => {
    setUser(null);
    setAccessToken(null);
    setRefreshToken(null);

    storage.remove("access_token");
    storage.remove("refresh_token");
  };

  return (
    <AuthContext.Provider value={{ user, login, logout, loading }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = (): AuthContextProps => {
  const context = useContext(AuthContext);

  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }

  return context;
};
