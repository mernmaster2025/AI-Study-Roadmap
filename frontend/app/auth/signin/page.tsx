"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { api, oauthLoginUrl, type OAuthProviders } from "@/lib/api";
import { useAuth } from "@/lib/auth";

export default function SignInPage() {
  const { login } = useAuth();
  const router = useRouter();
  const [providers, setProviders] = useState<OAuthProviders>({
    github: false,
    google: false,
  });

  useEffect(() => {
    api.oauthProviders().then(setProviders).catch(() => {});
  }, []);

  const demoLogin = async () => {
    await login();
    router.push("/dashboard");
  };

  const anyOAuth = providers.github || providers.google;

  return (
    <div className="mx-auto max-w-md py-16">
      <h1 className="mb-2 text-2xl font-bold">Sign in</h1>
      <p className="mb-8 text-gray-600">
        Sign in to track your progress across the roadmap.
      </p>

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
            className="flex w-full items-center justify-center gap-2 rounded-lg border px-4 py-3 font-medium hover:bg-gray-50"
          >
            Continue with Google
          </a>
        )}

        {anyOAuth && (
          <div className="flex items-center gap-3 py-2 text-sm text-gray-400">
            <div className="h-px flex-1 bg-gray-200" />
            or
            <div className="h-px flex-1 bg-gray-200" />
          </div>
        )}

        <button
          onClick={demoLogin}
          className="w-full rounded-lg bg-brand-600 px-4 py-3 font-medium text-white hover:bg-brand-700"
        >
          Continue as demo user
        </button>
      </div>

      {!anyOAuth && (
        <p className="mt-6 text-sm text-gray-500">
          GitHub/Google sign-in isn&apos;t configured on this server. Set the
          OAuth client credentials in the backend <code>.env</code> to enable
          them — the demo login works either way.
        </p>
      )}
    </div>
  );
}
