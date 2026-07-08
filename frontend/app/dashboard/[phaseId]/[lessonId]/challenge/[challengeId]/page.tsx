"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { api, type Lesson, type Challenge } from "@/lib/api";
import CodeEditor from "@/components/CodeEditor";

const DIFF_BADGE: Record<string, string> = {
  easy: "bg-green-100 text-green-700 dark:bg-green-900/40 dark:text-green-300",
  medium: "bg-amber-100 text-amber-700 dark:bg-amber-900/40 dark:text-amber-300",
  hard: "bg-red-100 text-red-700 dark:bg-red-900/40 dark:text-red-300",
};

export default function ChallengePage({
  params,
}: {
  params: { phaseId: string; lessonId: string; challengeId: string };
}) {
  const { phaseId, lessonId, challengeId } = params;
  const [lesson, setLesson] = useState<Lesson | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api
      .lesson(lessonId)
      .then(setLesson)
      .finally(() => setLoading(false));
  }, [lessonId]);

  if (loading) return <p className="text-gray-500 dark:text-gray-400">Loading…</p>;
  if (!lesson) return <p>Lesson not found.</p>;

  const idx = lesson.challenges.findIndex((c) => c.id === challengeId);
  const challenge: Challenge | undefined = lesson.challenges[idx];
  if (!challenge) return <p>Challenge not found.</p>;

  const prev = lesson.challenges[idx - 1];
  const next = lesson.challenges[idx + 1];
  const base = `/dashboard/${phaseId}/${lessonId}`;

  return (
    <div>
      <Link href={base} className="text-sm text-brand-600 hover:underline dark:text-brand-500">
        ← {lesson.title}
      </Link>

      <div className="mb-2 mt-3 flex items-center gap-3">
        <h1 className="text-2xl font-bold">{challenge.title}</h1>
        <span
          className={`rounded-full px-2.5 py-0.5 text-xs font-medium capitalize ${
            DIFF_BADGE[challenge.difficulty] ?? DIFF_BADGE.easy
          }`}
        >
          {challenge.difficulty}
        </span>
        <span className="text-sm text-gray-500 dark:text-gray-400">
          Challenge {idx + 1} of {lesson.challenges.length}
        </span>
      </div>

      <p className="mb-5 text-gray-700 dark:text-gray-300">{challenge.description}</p>

      <CodeEditor challenge={challenge} />

      {/* Prev / next challenge navigation */}
      <div className="mt-8 flex items-center justify-between border-t border-gray-200 pt-5 dark:border-gray-800">
        {prev ? (
          <Link
            href={`${base}/challenge/${prev.id}`}
            className="rounded-md border border-gray-200 px-4 py-2 text-sm hover:bg-gray-50 dark:border-gray-700 dark:hover:bg-gray-800"
          >
            ← {prev.title}
          </Link>
        ) : (
          <span />
        )}
        {next ? (
          <Link
            href={`${base}/challenge/${next.id}`}
            className="rounded-md border border-gray-200 px-4 py-2 text-sm hover:bg-gray-50 dark:border-gray-700 dark:hover:bg-gray-800"
          >
            {next.title} →
          </Link>
        ) : (
          <Link
            href={base}
            className="rounded-md bg-brand-600 px-4 py-2 text-sm font-medium text-white hover:bg-brand-700"
          >
            Back to lesson
          </Link>
        )}
      </div>
    </div>
  );
}
