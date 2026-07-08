"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { Highlight, themes } from "prism-react-renderer";
import { api, type Lesson } from "@/lib/api";
import Markdown from "@/components/Markdown";

const DIFF_BADGE: Record<string, string> = {
  easy: "bg-green-100 text-green-700 dark:bg-green-900/40 dark:text-green-300",
  medium: "bg-amber-100 text-amber-700 dark:bg-amber-900/40 dark:text-amber-300",
  hard: "bg-red-100 text-red-700 dark:bg-red-900/40 dark:text-red-300",
};

export default function LessonPage({
  params,
}: {
  params: { phaseId: string; lessonId: string };
}) {
  const { phaseId, lessonId } = params;
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

  return (
    <div>
      <Link
        href={`/dashboard/${phaseId}`}
        className="text-sm text-brand-600 hover:underline dark:text-brand-500"
      >
        ← Back to phase
      </Link>

      <h1 className="mt-3 text-3xl font-bold">{lesson.title}</h1>

      {/* Beginner-friendly intro (the gentle on-ramp) */}
      <div className="mt-4 rounded-xl border border-brand-200 bg-brand-50 p-6 dark:border-brand-500/30 dark:bg-brand-500/10">
        <Markdown className="prose-sm">{lesson.description}</Markdown>
      </div>

      {/* The technical deep-dive */}
      <div className="mt-6 rounded-xl border border-gray-200 bg-white p-6 dark:border-gray-800 dark:bg-gray-900">
        <Markdown>{lesson.content_markdown}</Markdown>
      </div>

      {/* Quiz CTA */}
      <div className="mt-6 flex items-center justify-between rounded-xl border border-brand-200 bg-brand-50 p-5 dark:border-brand-500/30 dark:bg-brand-500/10">
        <div>
          <p className="font-semibold">Check your understanding</p>
          <p className="text-sm text-gray-600 dark:text-gray-400">
            Take the quiz to test the key ideas from this lesson.
          </p>
        </div>
        <Link
          href={`/dashboard/${phaseId}/${lessonId}/quiz`}
          className="shrink-0 rounded-md bg-brand-600 px-5 py-2 font-medium text-white hover:bg-brand-700"
        >
          Take the quiz →
        </Link>
      </div>

      {/* Examples */}
      {lesson.examples.length > 0 && (
        <section className="mt-8">
          <h2 className="mb-3 text-xl font-bold">Examples</h2>
          <div className="space-y-4">
            {lesson.examples.map((ex, i) => (
              <div
                key={i}
                className="overflow-hidden rounded-lg border border-gray-200 dark:border-gray-800"
              >
                <div className="border-b border-gray-200 bg-gray-50 px-4 py-2 text-sm font-medium dark:border-gray-800 dark:bg-gray-800/60">
                  {ex.title}
                </div>
                <Highlight theme={themes.vsDark} code={ex.code} language={ex.language || "python"}>
                  {({ style, tokens, getLineProps, getTokenProps }) => (
                    <pre className="m-0 overflow-auto p-4 text-sm" style={style}>
                      {tokens.map((line, li) => (
                        <div key={li} {...getLineProps({ line })}>
                          {line.map((token, ti) => (
                            <span key={ti} {...getTokenProps({ token })} />
                          ))}
                        </div>
                      ))}
                    </pre>
                  )}
                </Highlight>
              </div>
            ))}
          </div>
        </section>
      )}

      {/* Challenges — as a list linking to each challenge */}
      {lesson.challenges.length > 0 && (
        <section className="mt-10">
          <h2 className="mb-3 text-xl font-bold">
            Challenges{" "}
            <span className="text-base font-normal text-gray-500 dark:text-gray-400">
              ({lesson.challenges.length})
            </span>
          </h2>
          <div className="space-y-3">
            {lesson.challenges.map((challenge, i) => (
              <Link
                key={challenge.id}
                href={`/dashboard/${phaseId}/${lessonId}/challenge/${challenge.id}`}
                className="group flex items-center gap-4 rounded-xl border border-gray-200 bg-white p-4 transition hover:border-brand-400 hover:shadow-md hover:shadow-black/5 dark:border-gray-800 dark:bg-gray-900 dark:hover:border-brand-500/50"
              >
                <div className="grid h-10 w-10 shrink-0 place-items-center rounded-lg bg-brand-50 font-bold text-brand-600 dark:bg-brand-500/10 dark:text-brand-400">
                  {i + 1}
                </div>
                <div className="min-w-0 flex-1">
                  <div className="flex items-center gap-2">
                    <span className="font-semibold">{challenge.title}</span>
                    <span
                      className={`rounded-full px-2 py-0.5 text-xs font-medium capitalize ${
                        DIFF_BADGE[challenge.difficulty] ?? DIFF_BADGE.easy
                      }`}
                    >
                      {challenge.difficulty}
                    </span>
                  </div>
                  <p className="mt-0.5 line-clamp-1 text-sm text-gray-600 dark:text-gray-400">
                    {challenge.description}
                  </p>
                </div>
                <span className="shrink-0 text-brand-600 transition group-hover:translate-x-0.5 dark:text-brand-500">
                  Solve →
                </span>
              </Link>
            ))}
          </div>
        </section>
      )}
    </div>
  );
}
