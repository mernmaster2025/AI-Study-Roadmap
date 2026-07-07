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

      <article className="prose mt-4 max-w-none">
        <div className="rounded-xl border bg-white p-6">
          <ReactMarkdown>{lesson.content_markdown}</ReactMarkdown>
        </div>
      </article>

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
