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
  access: string;
  refresh: string;
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
  const [authState, setAuthState] = useState<{
    user: UserProps | null;
    loading: boolean;
    initialized: boolean;
  }>({
    user: null,
    loading: true,
    initialized: false,
  });
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
      return data;
    } catch (error) {
      return null;
    }
  }, []);

  const login = async (username: string, password: string) => {
    setAuthState((prev) => ({ ...prev, loading: true }));

    try {
      await api.post(
        "/auth/login/",
        { username, password },
        { withCredentials: true }
      );

      const user = await fetchUserProfile();

      setAuthState({
        user,
        loading: false,
        initialized: true,
      });
      toast("Logged in successfully");
    } catch (error) {
      const message = axios.isAxiosError(error)
        ? error.response?.data?.message || error.message
        : "Login failed";
      toast(message);
      setAuthState((prev) => ({ ...prev, loading: false }));
    }
  };

  const logout = useCallback(async () => {
    try {
      api.post("/auth/logout/", {}, { withCredentials: true });
    } catch (error) {
      console.log("Failed to logout: ", error);
    } finally {
      setAuthState({
        user: null,
        loading: false,
        initialized: true,
      });
      processQueue(new Error("User logged out"));
    }
  }, [processQueue]);

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
        }).finally(() => {
          originalRequest.headers = originalRequest.headers || {};
          originalRequest.headers.Authorization = `Bearer ${api.defaults.headers.common.Authorization}`;
          return api(originalRequest);
        });
      }

      originalRequest._retry = true;
      isRefreshing.current = true;

      try {
        await api.post(
          "/auth/refresh/",
          {},
          {
            withCredentials: true,
          }
        );

        processQueue(null);
        return api(originalRequest);
      } catch (refreshError) {
        processQueue(refreshError);
        await logout();
        return Promise.reject(refreshError);
      } finally {
        isRefreshing.current = false;
      }
    },
    [logout, processQueue]
  );

  useEffect(() => {
    const requestInterceptor = api.interceptors.request.use((config) => {
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
  }, [handleAuthError]);

  useEffect(() => {
    const initializeAuth = async () => {
      try {
        if (document.cookie.includes('refresh_token')) {
          await api.post(
            "/auth/refresh/",
            {},
            {
              withCredentials: true,
            }
          );
        }
        const user = await fetchUserProfile();

        setAuthState({
          user,
          loading: false,
          initialized: true,
        });
      } catch (error) {
        setAuthState({
          user: null,
          loading: false,
          initialized: true,
        });
      }
    };

    initializeAuth();
  }, []);

  return (
    <AuthContext.Provider
      value={{
        user: authState.user,
        login,
        logout,
        loading: authState.loading,
      }}
    >
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
