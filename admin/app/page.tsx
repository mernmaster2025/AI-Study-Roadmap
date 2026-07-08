"use client";

import { useEffect, useState } from "react";
import Shell from "@/components/Shell";
import { api, type Stats } from "@/lib/api";

export default function DashboardPage() {
  return (
    <Shell>
      <Dashboard />
    </Shell>
  );
}

function Dashboard() {
  const [stats, setStats] = useState<Stats | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    api.stats().then(setStats).catch((e) => setError(e.message));
  }, []);

  if (error) return <p className="text-red-600">{error}</p>;
  if (!stats) return <p className="text-gray-500">Loading…</p>;

  const cards: { label: string; value: number; icon: string }[] = [
    { label: "Users", value: stats.users, icon: "👥" },
    { label: "Admins", value: stats.admins, icon: "🛡️" },
    { label: "Phases", value: stats.phases, icon: "🗺️" },
    { label: "Lessons", value: stats.lessons, icon: "📖" },
    { label: "Challenges", value: stats.challenges, icon: "🧩" },
    { label: "Quiz questions", value: stats.quiz_questions, icon: "❓" },
    { label: "Submissions", value: stats.submissions, icon: "📝" },
    { label: "Passed submissions", value: stats.passed_submissions, icon: "✅" },
    { label: "Quiz attempts", value: stats.quiz_attempts, icon: "🧠" },
  ];

  return (
    <div>
      <h1 className="mb-6 text-2xl font-bold">Dashboard</h1>
      <div className="grid grid-cols-2 gap-4 sm:grid-cols-3">
        {cards.map((c) => (
          <div key={c.label} className="rounded-xl border bg-white p-5">
            <div className="text-2xl">{c.icon}</div>
            <div className="mt-2 text-3xl font-bold">{c.value}</div>
            <div className="text-sm text-gray-500">{c.label}</div>
          </div>
        ))}
      </div>
    </div>
  );
}
