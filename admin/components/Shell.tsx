"use client";

import { useEffect } from "react";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { useAuth } from "@/lib/auth";

const NAV = [
  { href: "/", label: "Dashboard", icon: "📊" },
  { href: "/users", label: "Users", icon: "👥" },
  { href: "/content", label: "Content", icon: "📚" },
  { href: "/submissions", label: "Submissions", icon: "✅" },
];

/** Wraps protected admin pages: guards auth, renders sidebar + header. */
export default function Shell({ children }: { children: React.ReactNode }) {
  const { user, loading, logout } = useAuth();
  const router = useRouter();
  const pathname = usePathname();

  useEffect(() => {
    if (!loading && !user) router.replace("/login");
  }, [loading, user, router]);

  if (loading)
    return <div className="p-10 text-gray-500">Loading…</div>;
  if (!user) return null; // redirecting

  return (
    <div className="flex min-h-screen">
      <aside className="w-56 shrink-0 border-r bg-white">
        <div className="border-b px-5 py-4">
          <div className="font-bold text-brand-700">AI Study</div>
          <div className="text-xs text-gray-500">Admin panel</div>
        </div>
        <nav className="p-3">
          {NAV.map((n) => {
            const active =
              n.href === "/" ? pathname === "/" : pathname.startsWith(n.href);
            return (
              <Link
                key={n.href}
                href={n.href}
                className={`mb-1 flex items-center gap-2 rounded-md px-3 py-2 text-sm ${
                  active
                    ? "bg-brand-50 font-medium text-brand-700"
                    : "text-gray-600 hover:bg-gray-50"
                }`}
              >
                <span>{n.icon}</span>
                {n.label}
              </Link>
            );
          })}
        </nav>
      </aside>

      <div className="flex-1">
        <header className="flex items-center justify-between border-b bg-white px-6 py-3">
          <div />
          <div className="flex items-center gap-3 text-sm">
            <span className="text-gray-600">{user.email}</span>
            <button
              onClick={logout}
              className="rounded-md border px-3 py-1.5 hover:bg-gray-50"
            >
              Sign out
            </button>
          </div>
        </header>
        <main className="mx-auto max-w-6xl p-6">{children}</main>
      </div>
    </div>
  );
}
