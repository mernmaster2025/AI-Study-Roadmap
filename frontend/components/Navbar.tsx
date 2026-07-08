"use client";

import Link from "next/link";
import { useAuth } from "@/lib/auth";
import { useTheme } from "@/lib/theme";

export default function Navbar() {
  const { user, logout, loading } = useAuth();
  const { theme, toggle } = useTheme();

  return (
    <header className="border-b border-gray-200 bg-white/80 backdrop-blur dark:border-gray-800 dark:bg-gray-950/80">
      <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-3">
        <Link href="/" className="text-lg font-bold text-brand-600 dark:text-brand-500">
          AI Study Platform
        </Link>
        <nav className="flex items-center gap-3 text-sm">
          <Link
            href="/dashboard"
            className="text-gray-600 hover:text-gray-900 dark:text-gray-400 dark:hover:text-gray-100"
          >
            Dashboard
          </Link>
          <button
            onClick={toggle}
            aria-label="Toggle theme"
            className="rounded-md border border-gray-200 px-2 py-1.5 text-base hover:bg-gray-50 dark:border-gray-700 dark:hover:bg-gray-800"
          >
            {theme === "dark" ? "☀️" : "🌙"}
          </button>
          {loading ? null : user ? (
            <div className="flex items-center gap-3">
              {user.avatar_url ? (
                // eslint-disable-next-line @next/next/no-img-element
                <img src={user.avatar_url} alt={user.name} className="h-7 w-7 rounded-full" />
              ) : null}
              <span className="text-gray-600 dark:text-gray-400">{user.name}</span>
              <button
                onClick={logout}
                className="rounded-md border border-gray-200 px-3 py-1.5 hover:bg-gray-50 dark:border-gray-700 dark:hover:bg-gray-800"
              >
                Sign out
              </button>
            </div>
          ) : (
            <Link
              href="/auth/signin"
              className="rounded-md bg-brand-600 px-3 py-1.5 font-medium text-white hover:bg-brand-700"
            >
              Sign in
            </Link>
          )}
        </nav>
      </div>
    </header>
  );
}
