"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import ReactMarkdown from "react-markdown";
import { api, type PhaseDetail } from "@/lib/api";
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

  if (loading) return <p className="text-gray-500">Loading…</p>;
  if (!phase) return <p>Phase not found.</p>;

  return (
    <div>
      <Link href="/dashboard" className="text-sm text-brand-600 hover:underline">
        ← All phases
      </Link>
      <h1 className="mt-2 text-3xl font-bold">
        Phase {phase.phase_number}: {phase.title}
      </h1>

      <article className="prose prose-sm mt-4 max-w-none rounded-xl border bg-white p-6">
        <ReactMarkdown>{phase.description}</ReactMarkdown>
      </article>

      <h2 className="mt-8 mb-3 text-xl font-bold">Lessons</h2>
      <div className="space-y-3">
        {phase.lessons.map((lesson) => (
          <Link
            key={lesson.id}
            href={`/dashboard/${phase.id}/${lesson.id}`}
            className="flex items-center justify-between rounded-xl border bg-white p-5 transition hover:shadow-md"
          >
            <div>
              <div className="text-xs font-medium uppercase tracking-wide text-brand-600">
                Lesson {lesson.lesson_number}
              </div>
              <div className="font-semibold">{lesson.title}</div>
              <div className="text-sm text-gray-600">
                {teaser(lesson.description)}
              </div>
            </div>
            <span className="text-sm text-gray-400">
              ~{lesson.estimated_minutes} min
            </span>
          </Link>
        ))}
      </div>
    </div>
  );
}
