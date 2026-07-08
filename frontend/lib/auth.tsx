"use client";

// Lightweight client auth context backed by the backend dev-login + JWT.
// This is the seam where NextAuth (GitHub/Google) drops in later: replace
// `login` with signIn() and read the session instead of localStorage.
import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useState,
} from "react";
import { api, getToken, setToken, type User } from "./api";

interface AuthState {
  user: User | null;
  loading: boolean;
  /** Passwordless demo sign-in (dev-login). */
  login: (email?: string, name?: string) => Promise<void>;
  /** Email/password sign-in. */
  loginWithPassword: (email: string, password: string) => Promise<void>;
  /** Create an account with email/password. */
  registerWithPassword: (
    email: string,
    name: string,
    password: string
  ) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthState | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Restore a session from a persisted token on first load.
    if (!getToken()) {
      setLoading(false);
      return;
    }
    api
      .me()
      .then(setUser)
      .catch(() => setToken(null))
      .finally(() => setLoading(false));
  }, []);

  const login = useCallback(
    async (email = "demo@studyplatform.dev", name = "Demo Learner") => {
      const { access_token, user } = await api.devLogin(email, name);
      setToken(access_token);
      setUser(user);
    },
    []
  );

  const loginWithPassword = useCallback(
    async (email: string, password: string) => {
      const { access_token, user } = await api.login(email, password);
      setToken(access_token);
      setUser(user);
    },
    []
  );

  const registerWithPassword = useCallback(
    async (email: string, name: string, password: string) => {
      const { access_token, user } = await api.register(email, name, password);
      setToken(access_token);
      setUser(user);
    },
    []
  );

  const logout = useCallback(() => {
    setToken(null);
    setUser(null);
  }, []);

  return (
    <AuthContext.Provider
      value={{
        user,
        loading,
        login,
        loginWithPassword,
        registerWithPassword,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within an AuthProvider");
  return ctx;
}
