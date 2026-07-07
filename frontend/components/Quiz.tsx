"use client";

import { useState } from "react";
import { api, type Quiz as QuizData, type QuizResult } from "@/lib/api";
import { useAuth } from "@/lib/auth";
import ProgressBar from "@/components/ProgressBar";

export default function Quiz({ quiz }: { quiz: QuizData }) {
  const { user, login } = useAuth();
  const [answers, setAnswers] = useState<Record<string, string>>({});
  const [index, setIndex] = useState(0);
  const [result, setResult] = useState<QuizResult | null>(null);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const questions = quiz.questions;
  const current = questions[index];
  const answered = Object.keys(answers).length;

  const setAnswer = (value: string) =>
    setAnswers((a) => ({ ...a, [current.id]: value }));

  const submit = async () => {
    setSubmitting(true);
    setError(null);
    try {
      if (!user) await login();
      setResult(await api.submitQuiz(quiz.lesson_id, answers));
    } catch (e) {
      setError(e instanceof Error ? e.message : "Submission failed");
    } finally {
      setSubmitting(false);
    }
  };

  const reset = () => {
    setAnswers({});
    setIndex(0);
    setResult(null);
  };

  if (questions.length === 0) {
    return <p className="text-gray-500">This lesson has no quiz yet.</p>;
  }

  // ---- Results view ----
  if (result) {
    return (
      <div>
        <div className="mb-6 rounded-xl border bg-white p-6 text-center">
          <p className="text-5xl font-extrabold">{result.score}%</p>
          <p className="mt-1 text-gray-600">
            {result.correct_count}/{result.total} correct · attempt{" "}
            {result.attempts}
          </p>
          <p
            className={`mt-3 font-medium ${
              result.passed ? "text-green-600" : "text-orange-600"
            }`}
          >
            {result.passed
              ? "🎉 Passed! (80%+)"
              : "Keep at it — review below and retake."}
          </p>
        </div>

        <div className="space-y-4">
          {result.detailed_results.map((r, i) => (
            <div key={r.id} className="rounded-lg border bg-white p-4">
              <p className="font-medium">
                {i + 1}. {r.text}
              </p>
              <p className={r.correct ? "text-green-700" : "text-red-700"}>
                Your answer: {r.user_answer ?? "(blank)"}{" "}
                {r.correct ? "✓" : "✗"}
              </p>
              {!r.correct && (
                <p className="text-green-700">
                  Correct answer: {r.correct_answer}
                </p>
              )}
              <p className="mt-1 text-sm text-gray-600">{r.explanation}</p>
            </div>
          ))}
        </div>

        <button
          onClick={reset}
          className="mt-6 rounded-md bg-brand-600 px-5 py-2 font-medium text-white hover:bg-brand-700"
        >
          Retake quiz
        </button>
      </div>
    );
  }

  // ---- Question view ----
  return (
    <div className="max-w-2xl">
      <div className="mb-4">
        <p className="mb-1 text-sm text-gray-500">
          Question {index + 1} of {questions.length} · {answered} answered
        </p>
        <ProgressBar value={((index + 1) / questions.length) * 100} />
      </div>

      <h3 className="mb-4 text-lg font-semibold">{current.text}</h3>

      {current.type === "multiple-choice" ? (
        <div className="space-y-2">
          {current.options.map((opt) => (
            <label
              key={opt}
              className={`flex cursor-pointer items-center rounded-lg border p-3 hover:bg-gray-50 ${
                answers[current.id] === opt ? "border-brand-600 bg-brand-50" : ""
              }`}
            >
              <input
                type="radio"
                name={current.id}
                value={opt}
                checked={answers[current.id] === opt}
                onChange={(e) => setAnswer(e.target.value)}
                className="mr-3"
              />
              {opt}
            </label>
          ))}
        </div>
      ) : (
        <input
          type="text"
          value={answers[current.id] ?? ""}
          onChange={(e) => setAnswer(e.target.value)}
          placeholder="Type your answer…"
          className="w-full rounded-lg border p-3"
        />
      )}

      {error && <p className="mt-3 text-sm text-red-600">{error}</p>}

      <div className="mt-6 flex items-center justify-between">
        <button
          onClick={() => setIndex((i) => Math.max(0, i - 1))}
          disabled={index === 0}
          className="rounded-md bg-gray-200 px-4 py-2 disabled:opacity-50"
        >
          Previous
        </button>

        {index === questions.length - 1 ? (
          <button
            onClick={submit}
            disabled={submitting || answered < questions.length}
            className="rounded-md bg-green-600 px-6 py-2 font-medium text-white hover:bg-green-700 disabled:opacity-50"
            title={
              answered < questions.length
                ? "Answer every question first"
                : undefined
            }
          >
            {submitting ? "Submitting…" : "Submit quiz"}
          </button>
        ) : (
          <button
            onClick={() => setIndex((i) => Math.min(questions.length - 1, i + 1))}
            className="rounded-md bg-brand-600 px-4 py-2 text-white hover:bg-brand-700"
          >
            Next
          </button>
        )}
      </div>
    </div>
  );
}
