"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { api, oauthLoginUrl, type OAuthProviders } from "@/lib/api";
import { useAuth } from "@/lib/auth";

type Mode = "login" | "register";

export default function SignInPage() {
  const { login, loginWithPassword, registerWithPassword } = useAuth();
  const router = useRouter();
  const [providers, setProviders] = useState<OAuthProviders>({
    github: false,
    google: false,
  });

  const [mode, setMode] = useState<Mode>("login");
  const [email, setEmail] = useState("");
  const [name, setName] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    api.oauthProviders().then(setProviders).catch(() => {});
  }, []);

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setBusy(true);
    try {
      if (mode === "register") {
        await registerWithPassword(email, name, password);
      } else {
        await loginWithPassword(email, password);
      }
      router.push("/dashboard");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong");
    } finally {
      setBusy(false);
    }
  };

  const demoLogin = async () => {
    setError(null);
    setBusy(true);
    try {
      await login();
      router.push("/dashboard");
    } finally {
      setBusy(false);
    }
  };

  const anyOAuth = providers.github || providers.google;

  return (
    <div className="mx-auto max-w-md py-14">
      <h1 className="mb-1 text-2xl font-bold">
        {mode === "login" ? "Sign in" : "Create your account"}
      </h1>
      <p className="mb-6 text-gray-600 dark:text-gray-400">
        Track your progress across the roadmap.
      </p>

      {/* Login / Register toggle */}
      <div className="mb-6 grid grid-cols-2 rounded-lg bg-gray-100 p-1 text-sm font-medium dark:bg-gray-800">
        {(["login", "register"] as Mode[]).map((m) => (
          <button
            key={m}
            onClick={() => {
              setMode(m);
              setError(null);
            }}
            className={`rounded-md py-2 transition ${
              mode === m
                ? "bg-white shadow dark:bg-gray-900"
                : "text-gray-500 hover:text-gray-800 dark:text-gray-400 dark:hover:text-gray-200"
            }`}
          >
            {m === "login" ? "Sign in" : "Create account"}
          </button>
        ))}
      </div>

      <form onSubmit={submit} className="space-y-3">
        {mode === "register" && (
          <input
            type="text"
            required
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder="Name"
            className="w-full rounded-lg border border-gray-200 bg-white p-3 dark:border-gray-700 dark:bg-gray-900"
          />
        )}
        <input
          type="email"
          required
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="Email"
          autoComplete="email"
          className="w-full rounded-lg border border-gray-200 bg-white p-3 dark:border-gray-700 dark:bg-gray-900"
        />
        <input
          type="password"
          required
          minLength={mode === "register" ? 8 : undefined}
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder={mode === "register" ? "Password (min 8 characters)" : "Password"}
          autoComplete={mode === "register" ? "new-password" : "current-password"}
          className="w-full rounded-lg border border-gray-200 bg-white p-3 dark:border-gray-700 dark:bg-gray-900"
        />

        {error && <p className="text-sm text-red-600">{error}</p>}

        <button
          type="submit"
          disabled={busy}
          className="w-full rounded-lg bg-brand-600 px-4 py-3 font-medium text-white hover:bg-brand-700 disabled:opacity-50"
        >
          {busy
            ? "Please wait…"
            : mode === "login"
              ? "Sign in"
              : "Create account"}
        </button>
      </form>

      {/* Divider */}
      <div className="flex items-center gap-3 py-5 text-sm text-gray-400">
        <div className="h-px flex-1 bg-gray-200 dark:bg-gray-800" />
        or
        <div className="h-px flex-1 bg-gray-200 dark:bg-gray-800" />
      </div>

      <div className="space-y-3">
        {providers.github && (
          <a
            href={oauthLoginUrl("github")}
            className="flex w-full items-center justify-center gap-2 rounded-lg bg-gray-900 px-4 py-3 font-medium text-white hover:bg-black"
          >
            Continue with GitHub
          </a>
        )}
        {providers.google && (
          <a
            href={oauthLoginUrl("google")}
            className="flex w-full items-center justify-center gap-2 rounded-lg border border-gray-200 px-4 py-3 font-medium hover:bg-gray-50 dark:border-gray-700 dark:hover:bg-gray-800"
          >
            Continue with Google
          </a>
        )}
        <button
          onClick={demoLogin}
          disabled={busy}
          className="w-full rounded-lg border border-gray-200 px-4 py-3 font-medium hover:bg-gray-50 disabled:opacity-50 dark:border-gray-700 dark:hover:bg-gray-800"
        >
          Continue as demo user
        </button>
      </div>

      {!anyOAuth && (
        <p className="mt-6 text-sm text-gray-500 dark:text-gray-400">
          GitHub/Google sign-in isn&apos;t configured on this server — add the
          OAuth credentials in the backend <code>.env</code> to enable them.
          Email/password and the demo login work either way.
        </p>
      )}
    </div>
  );
}
