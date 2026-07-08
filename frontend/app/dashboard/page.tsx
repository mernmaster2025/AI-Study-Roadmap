"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import {
  api,
  type Phase,
  type ProgressOverview,
  type PhaseProgress,
} from "@/lib/api";
import { useAuth } from "@/lib/auth";
import ProgressBar from "@/components/ProgressBar";
import { teaser } from "@/lib/text";

export default function DashboardPage() {
  const { user, login, loading: authLoading } = useAuth();
  const [phases, setPhases] = useState<Phase[]>([]);
  const [progress, setProgress] = useState<ProgressOverview | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (authLoading) return;
    const load = async () => {
      setLoading(true);
      try {
        const phaseList = await api.phases();
        setPhases(phaseList);
        if (user) setProgress(await api.progress());
      } finally {
        setLoading(false);
      }
    };
    load();
  }, [user, authLoading]);

  const progressByPhase = new Map<string, PhaseProgress>(
    (progress?.phases ?? []).map((p) => [p.phase_id, p])
  );

  if (loading) return <p className="text-gray-500 dark:text-gray-400">Loading…</p>;

  return (
    <div>
      <div className="mb-8 flex items-end justify-between">
        <div>
          <h1 className="text-3xl font-bold">Your Roadmap</h1>
          <p className="text-gray-600 dark:text-gray-400">Pick a phase to start learning.</p>
        </div>
        {!user && (
          <button
            onClick={() => login()}
            className="rounded-md bg-brand-600 px-4 py-2 text-sm font-medium text-white hover:bg-brand-700"
          >
            Sign in to track progress
          </button>
        )}
      </div>

      {progress && (
        <div className="mb-8 grid grid-cols-2 gap-4 sm:grid-cols-4">
          <StatCard label="Overall completion" value={`${progress.overall_percentage}%`} icon="🎯" />
          <StatCard label="Challenges solved" value={progress.challenges_solved} icon="✅" />
          <StatCard label="Quizzes passed" value={progress.quizzes_passed} icon="🧠" />
          <StatCard label="Phases" value={phases.length} icon="🗺️" />
        </div>
      )}

      <div className="space-y-4">
        {phases.map((phase) => {
          const pp = progressByPhase.get(phase.id);
          return (
            <Link
              key={phase.id}
              href={`/dashboard/${phase.id}`}
              className="block rounded-xl border border-gray-200 bg-white p-6 transition hover:shadow-md hover:shadow-black/5 dark:border-gray-800 dark:bg-gray-900 dark:hover:border-gray-700"
            >
              <div className="flex items-center justify-between">
                <h2 className="text-lg font-semibold">
                  Phase {phase.phase_number}: {phase.title}
                </h2>
                <span className="text-sm text-gray-500 dark:text-gray-400">
                  ~{phase.estimated_hours}h
                </span>
              </div>
              <p className="mt-1 text-sm text-gray-600 dark:text-gray-400">
                {teaser(phase.description, 180)}
              </p>
              {pp && (
                <div className="mt-4">
                  <div className="mb-1 flex justify-between text-xs text-gray-500 dark:text-gray-400">
                    <span>
                      {pp.challenges_solved}/{pp.total_challenges} challenges
                      {pp.total_quizzes > 0 &&
                        ` · ${pp.quizzes_passed}/${pp.total_quizzes} quizzes`}
                    </span>
                    <span>{pp.progress_percentage}%</span>
                  </div>
                  <ProgressBar value={pp.progress_percentage} />
                </div>
              )}
            </Link>
          );
        })}
      </div>
    </div>
  );
}

function StatCard({
  label,
  value,
  icon,
}: {
  label: string;
  value: string | number;
  icon: string;
}) {
  return (
    <div className="rounded-xl border border-gray-200 bg-white p-5 dark:border-gray-800 dark:bg-gray-900">
      <div className="text-2xl">{icon}</div>
      <div className="mt-2 text-2xl font-bold">{value}</div>
      <div className="text-sm text-gray-500 dark:text-gray-400">{label}</div>
    </div>
  );
}
