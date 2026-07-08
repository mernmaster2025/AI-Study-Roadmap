"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import ReactMarkdown from "react-markdown";
import { Highlight, themes } from "prism-react-renderer";
import { api, type Lesson } from "@/lib/api";
import CodeEditor from "@/components/CodeEditor";

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

  if (loading) return <p className="text-gray-500">Loading…</p>;
  if (!lesson) return <p>Lesson not found.</p>;

  return (
    <div>
      <Link
        href={`/dashboard/${phaseId}`}
        className="text-sm text-brand-600 hover:underline"
      >
        ← Back to phase
      </Link>

      <h1 className="mt-3 text-3xl font-bold">{lesson.title}</h1>

      {/* Beginner-friendly intro (the gentle on-ramp) */}
      <article className="prose prose-sm mt-4 max-w-none rounded-xl border border-brand-100 bg-brand-50 p-6">
        <ReactMarkdown>{lesson.description}</ReactMarkdown>
      </article>

      {/* The technical deep-dive */}
      <article className="prose mt-6 max-w-none">
        <div className="rounded-xl border bg-white p-6">
          <ReactMarkdown>{lesson.content_markdown}</ReactMarkdown>
        </div>
      </article>

      <div className="mt-6 flex items-center justify-between rounded-xl border border-brand-100 bg-brand-50 p-5">
        <div>
          <p className="font-semibold">Check your understanding</p>
          <p className="text-sm text-gray-600">
            Take the quiz to test the key ideas from this lesson.
          </p>
        </div>
        <Link
          href={`/dashboard/${phaseId}/${lessonId}/quiz`}
          className="rounded-md bg-brand-600 px-5 py-2 font-medium text-white hover:bg-brand-700"
        >
          Take the quiz →
        </Link>
      </div>

      {lesson.examples.length > 0 && (
        <section className="mt-8">
          <h2 className="mb-3 text-xl font-bold">Examples</h2>
          <div className="space-y-4">
            {lesson.examples.map((ex, i) => (
              <div key={i} className="overflow-hidden rounded-lg border">
                <div className="border-b bg-gray-50 px-4 py-2 text-sm font-medium">
                  {ex.title}
                </div>
                <Highlight
                  theme={themes.vsDark}
                  code={ex.code}
                  language={ex.language || "python"}
                >
                  {({ style, tokens, getLineProps, getTokenProps }) => (
                    <pre
                      className="m-0 overflow-auto p-4 text-sm"
                      style={style}
                    >
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

      {lesson.challenges.map((challenge) => (
        <section key={challenge.id} className="mt-10">
          <div className="mb-4 flex items-center gap-3">
            <h2 className="text-xl font-bold">Challenge: {challenge.title}</h2>
            <span className="rounded-full bg-gray-100 px-2.5 py-0.5 text-xs font-medium capitalize text-gray-600">
              {challenge.difficulty}
            </span>
          </div>
          <p className="mb-4 text-gray-700">{challenge.description}</p>
          <CodeEditor challenge={challenge} />
        </section>
      ))}
    </div>
  );
}
