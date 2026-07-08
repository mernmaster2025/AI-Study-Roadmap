"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { api, type PhaseDetail } from "@/lib/api";
import Markdown from "@/components/Markdown";
import { teaser } from "@/lib/text";

export default function PhasePage({
  params,
}: {
  params: { phaseId: string };
}) {
  const { phaseId } = params;
  const [phase, setPhase] = useState<PhaseDetail | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api
      .phase(phaseId)
      .then(setPhase)
      .finally(() => setLoading(false));
  }, [phaseId]);

  if (loading) return <p className="text-gray-500 dark:text-gray-400">Loading…</p>;
  if (!phase) return <p>Phase not found.</p>;

  return (
    <div>
      <Link href="/dashboard" className="text-sm text-brand-600 hover:underline dark:text-brand-500">
        ← All phases
      </Link>
      <h1 className="mt-2 text-3xl font-bold">
        Phase {phase.phase_number}: {phase.title}
      </h1>

      <div className="mt-4 rounded-xl border border-gray-200 bg-white p-6 dark:border-gray-800 dark:bg-gray-900">
        <Markdown className="prose-sm">{phase.description}</Markdown>
      </div>

      <h2 className="mb-3 mt-8 text-xl font-bold">Lessons</h2>
      <div className="space-y-3">
        {phase.lessons.map((lesson) => (
          <Link
            key={lesson.id}
            href={`/dashboard/${phase.id}/${lesson.id}`}
            className="flex items-center justify-between rounded-xl border border-gray-200 bg-white p-5 transition hover:shadow-md hover:shadow-black/5 dark:border-gray-800 dark:bg-gray-900 dark:hover:border-gray-700"
          >
            <div>
              <div className="text-xs font-medium uppercase tracking-wide text-brand-600 dark:text-brand-500">
                Lesson {lesson.lesson_number}
              </div>
              <div className="font-semibold">{lesson.title}</div>
              <div className="text-sm text-gray-600 dark:text-gray-400">
                {teaser(lesson.description)}
              </div>
            </div>
            <span className="shrink-0 pl-4 text-sm text-gray-400 dark:text-gray-500">
              ~{lesson.estimated_minutes} min
            </span>
          </Link>
        ))}
      </div>
    </div>
  );
}
