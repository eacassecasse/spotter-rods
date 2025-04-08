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

const AuthContext = createContext<AuthContextProps | undefined>(undefined);

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
  const [user, setUser] = useState<UserProps | null>(null);
  const [accessToken, setAccessToken] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [initialized, setInitialized] = useState(false);
  const isRefreshing = useRef(false);
  const failedQueue = useRef<
    Array<{
      resolve: (token: string) => void;
      reject: (error: any) => void;
    }>
  >([]);

  const processQueue = useCallback(
    (error: any, token: string | null = null) => {
      failedQueue.current.forEach((promise) => {
        token ? promise.resolve(token) : promise.reject(error);
      });

      failedQueue.current = [];
    },
    []
  );

  const fetchUserProfile = useCallback(async () => {
    try {
      const { data } = await api.get("/auth/profile");
      setUser(data);
    } catch (error) {
      logout();
    } finally {
      setLoading(false);
    }
  }, []);

  const login = async (username: string, password: string) => {
    if (!initialized) return;

    setLoading(true);
    try {
      const { data }: { data: LoginResponseProps } = await api.post(
        "/auth/login/",
        { username, password },
        { withCredentials: true }
      );

      setAccessToken(data.accessToken);
      api.defaults.headers.common.Authorization = `Bearer ${data.accessToken}`;

      await new Promise((resolve) => setTimeout(resolve, 50));

      await fetchUserProfile();
      console.log("Cookies => ", document.cookie);
      toast("Logged in successfully");
    } catch (error) {
      const message = axios.isAxiosError(error)
        ? error.response?.data?.message || error.message
        : "Login failed";
      toast(message);
    } finally {
      setLoading(false);
    }
  };

  const logout = useCallback(() => {
    setUser(null);
    setAccessToken(null);
    setLoading(false);
    api.defaults.headers.common.Authorization = "";
    api.post("/auth/logout/", {}, { withCredentials: true });
  }, []);

  const handleAuthError = useCallback(
    async (error: any) => {
      const originalRequest: AxiosRequestConfig & { _retry?: boolean } =
        error.config;

      if (error.response?.status !== 401 || originalRequest._retry) {
        return Promise.reject(error);
      }

      if (isRefreshing.current) {
        return new Promise((resolve, reject) => {
          failedQueue.current.push({ resolve, reject });
        }).then((token: unknown) => {
          originalRequest.headers = originalRequest.headers || {};
          originalRequest.headers.Authorization = `Bearer ${token}`;
          return api(originalRequest);
        });
      }

      originalRequest._retry = true;
      isRefreshing.current = true;

      try {
        console.log("Token expired, refreshing");
        const { data } = await api.post(
          "/auth/refresh/",
          {},
          {
            withCredentials: true,
          }
        );

        const { accessToken: newAccessToken } = data;

        setAccessToken(newAccessToken);
        api.defaults.headers.common.Authorization = `Bearer ${newAccessToken}`;
        processQueue(null, newAccessToken);

        originalRequest.headers = originalRequest.headers || {};
        originalRequest.headers.Authorization = `Bearer ${newAccessToken}`;

        return api(originalRequest);
      } catch (refreshError) {
        processQueue(refreshError, null);
        logout();
        return Promise.reject(refreshError);
      } finally {
        isRefreshing.current = false;
      }
    },
    [logout, processQueue]
  );

  useEffect(() => {
    const requestInterceptor = api.interceptors.request.use((config) => {
      if (accessToken) {
        config.headers.Authorization = `Bearer ${accessToken}`;
      }
      config.withCredentials = true;
      return config;
    });

    const responseInterceptor = api.interceptors.response.use(
      (response: AxiosResponse) => response,
      handleAuthError
    );

    return () => {
      api.interceptors.request.eject(requestInterceptor);
      api.interceptors.request.eject(responseInterceptor);
    };
  }, [accessToken, handleAuthError]);

  useEffect(() => {
    const initializeAuth = async () => {
      try {
        if (document.cookie.includes("refresh_token")) {
          const { data } = await api.post(
            "/auth/refresh",
            {},
            {
              withCredentials: true,
            }
          );

          setAccessToken(data.accessToken);
          api.defaults.headers.common.Authorization = `Bearer ${data.accessToken}`;
          await fetchUserProfile();
        }
      } catch (error) {
        logout();
      } finally {
        setLoading(false);
        setInitialized(true);
      }
    };

    initializeAuth();
  }, [fetchUserProfile, logout]);

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
