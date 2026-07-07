"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { api, type Quiz as QuizData } from "@/lib/api";
import Quiz from "@/components/Quiz";

export default function QuizPage({
  params,
}: {
  params: { phaseId: string; lessonId: string };
}) {
  const { phaseId, lessonId } = params;
  const [quiz, setQuiz] = useState<QuizData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api
      .quiz(lessonId)
      .then(setQuiz)
      .finally(() => setLoading(false));
  }, [lessonId]);

  if (loading) return <p className="text-gray-500">Loading…</p>;

  return (
    <div>
      <Link
        href={`/dashboard/${phaseId}/${lessonId}`}
        className="text-sm text-brand-600 hover:underline"
      >
        ← Back to lesson
      </Link>
      <h1 className="mb-6 mt-2 text-2xl font-bold">Lesson Quiz</h1>
      {quiz && <Quiz quiz={quiz} />}
    </div>
  );
}
