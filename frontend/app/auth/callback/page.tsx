"use client";

import { useEffect, useState } from "react";
import { setToken } from "@/lib/api";

// The backend OAuth callback redirects here with ?token=... (or ?error=...).
// We persist the token and hard-navigate to the dashboard so the AuthProvider
// re-initialises and picks up the session.
export default function OAuthCallbackPage() {
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const token = params.get("token");
    const err = params.get("error");

    if (token) {
      setToken(token);
      window.location.replace("/dashboard");
    } else {
      setError(err ?? "No token returned from the provider.");
    }
  }, []);

  return (
    <div className="mx-auto max-w-md py-20 text-center">
      {error ? (
        <>
          <h1 className="text-xl font-bold text-red-600 dark:text-red-400">Sign-in failed</h1>
          <p className="mt-2 text-gray-600 dark:text-gray-400">{error}</p>
          <a href="/auth/signin" className="mt-4 inline-block text-brand-600 hover:underline dark:text-brand-500">
            Try again
          </a>
        </>
      ) : (
        <p className="text-gray-500 dark:text-gray-400">Signing you in…</p>
      )}
    </div>
  );
}
