"use client";

import Link from "next/link";
import { useAuth } from "@/lib/auth";

export default function Navbar() {
  const { user, login, logout, loading } = useAuth();

  return (
    <header className="border-b bg-white">
      <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-3">
        <Link href="/" className="text-lg font-bold text-brand-700">
          AI Study Platform
        </Link>
        <nav className="flex items-center gap-4 text-sm">
          <Link href="/dashboard" className="text-gray-600 hover:text-gray-900">
            Dashboard
          </Link>
          {loading ? null : user ? (
            <div className="flex items-center gap-3">
              <span className="text-gray-600">{user.name}</span>
              <button
                onClick={logout}
                className="rounded-md border px-3 py-1.5 hover:bg-gray-50"
              >
                Sign out
              </button>
            </div>
          ) : (
            <button
              onClick={() => login()}
              className="rounded-md bg-brand-600 px-3 py-1.5 font-medium text-white hover:bg-brand-700"
            >
              Sign in (demo)
            </button>
          )}
        </nav>
      </div>
    </header>
  );
}
