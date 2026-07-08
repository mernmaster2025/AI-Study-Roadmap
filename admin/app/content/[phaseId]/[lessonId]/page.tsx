"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import Shell from "@/components/Shell";
import { api, type Challenge, type Lesson, type QuizQuestion } from "@/lib/api";

export default function LessonAdminPage({
  params,
}: {
  params: { phaseId: string; lessonId: string };
}) {
  return (
    <Shell>
      <LessonAdmin phaseId={params.phaseId} lessonId={params.lessonId} />
    </Shell>
  );
}

/** A textarea that edits a JSON value as text, reporting parse errors on save. */
function jsonText(value: unknown): string {
  return JSON.stringify(value ?? [], null, 2);
}

function LessonAdmin({ phaseId, lessonId }: { phaseId: string; lessonId: string }) {
  const [lesson, setLesson] = useState<Lesson | null>(null);
  const [challenges, setChallenges] = useState<Challenge[]>([]);
  const [quiz, setQuiz] = useState<QuizQuestion[]>([]);
  const [loading, setLoading] = useState(true);
  const [saved, setSaved] = useState(false);

  const reload = async () => {
    const [l, c, q] = await Promise.all([
      api.lesson(lessonId),
      api.challenges(lessonId),
      api.quiz(lessonId),
    ]);
    setLesson(l);
    setChallenges(c);
    setQuiz(q);
  };
  useEffect(() => {
    reload().finally(() => setLoading(false));
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [lessonId]);

  const saveLesson = async () => {
    if (!lesson) return;
    await api.updateLesson(lesson.id, {
      title: lesson.title,
      description: lesson.description,
      content_markdown: lesson.content_markdown,
      estimated_minutes: lesson.estimated_minutes,
      order: lesson.order,
    });
    setSaved(true);
    setTimeout(() => setSaved(false), 1500);
  };

  if (loading) return <p className="text-gray-500">Loading…</p>;
  if (!lesson) return <p>Lesson not found.</p>;

  return (
    <div>
      <Link href={`/content/${phaseId}`} className="text-sm text-brand-600 hover:underline">
        ← Back to phase
      </Link>
      <h1 className="mb-4 mt-2 text-2xl font-bold">Edit lesson</h1>

      {/* Lesson fields */}
      <div className="mb-8 space-y-3 rounded-xl border bg-white p-5">
        <label className="block text-sm">
          <span className="mb-1 block text-gray-500">Title</span>
          <input value={lesson.title} onChange={(e) => setLesson({ ...lesson, title: e.target.value })}
            className="w-full rounded-md border p-2" />
        </label>
        <div className="flex gap-3">
          <label className="w-40 text-sm">
            <span className="mb-1 block text-gray-500">Estimated minutes</span>
            <input type="number" value={lesson.estimated_minutes}
              onChange={(e) => setLesson({ ...lesson, estimated_minutes: Number(e.target.value) })}
              className="w-full rounded-md border p-2" />
          </label>
          <label className="w-28 text-sm">
            <span className="mb-1 block text-gray-500">Order</span>
            <input type="number" value={lesson.order}
              onChange={(e) => setLesson({ ...lesson, order: Number(e.target.value) })}
              className="w-full rounded-md border p-2" />
          </label>
        </div>
        <label className="block text-sm">
          <span className="mb-1 block text-gray-500">Description (Markdown — beginner intro)</span>
          <textarea value={lesson.description}
            onChange={(e) => setLesson({ ...lesson, description: e.target.value })}
            className="h-40 w-full rounded-md border p-2 font-mono text-xs" />
        </label>
        <label className="block text-sm">
          <span className="mb-1 block text-gray-500">Content (Markdown — deep dive)</span>
          <textarea value={lesson.content_markdown}
            onChange={(e) => setLesson({ ...lesson, content_markdown: e.target.value })}
            className="h-72 w-full rounded-md border p-2 font-mono text-xs" />
        </label>
        <div className="flex items-center gap-3">
          <button onClick={saveLesson}
            className="rounded-md bg-brand-600 px-5 py-2 text-sm font-medium text-white hover:bg-brand-700">
            Save lesson
          </button>
          {saved && <span className="text-sm text-green-600">Saved ✓</span>}
        </div>
      </div>

      {/* Challenges */}
      <div className="mb-3 flex items-center justify-between">
        <h2 className="text-xl font-bold">Challenges ({challenges.length})</h2>
        <button
          onClick={async () => {
            await api.createChallenge({
              lesson_id: lessonId, title: "New challenge", difficulty: "easy",
              starter_code: "def solve():\n    pass\n", solution_code: "", hints: [],
              test_cases: [], order: challenges.length,
            });
            reload();
          }}
          className="rounded-md border px-3 py-1.5 text-sm hover:bg-gray-50"
        >
          + Add challenge
        </button>
      </div>
      <div className="space-y-4">
        {challenges.map((c) => (
          <ChallengeEditor key={c.id} challenge={c} onChanged={reload} />
        ))}
      </div>

      {/* Quiz */}
      <div className="mb-3 mt-10 flex items-center justify-between">
        <h2 className="text-xl font-bold">Quiz questions ({quiz.length})</h2>
        <button
          onClick={async () => {
            await api.createQuiz({
              lesson_id: lessonId, type: "multiple-choice", text: "New question",
              options: ["A", "B"], correct_answer: "A", explanation: "", order: quiz.length,
            });
            reload();
          }}
          className="rounded-md border px-3 py-1.5 text-sm hover:bg-gray-50"
        >
          + Add question
        </button>
      </div>
      <div className="space-y-4">
        {quiz.map((q) => (
          <QuizEditor key={q.id} question={q} onChanged={reload} />
        ))}
      </div>
    </div>
  );
}

function ChallengeEditor({ challenge, onChanged }: { challenge: Challenge; onChanged: () => void }) {
  const [c, setC] = useState(challenge);
  const [testCases, setTestCases] = useState(jsonText(challenge.test_cases));
  const [hints, setHints] = useState(jsonText(challenge.hints));
  const [msg, setMsg] = useState<string | null>(null);

  const save = async () => {
    let tc: unknown, hn: unknown;
    try {
      tc = JSON.parse(testCases);
      hn = JSON.parse(hints);
    } catch {
      setMsg("Invalid JSON in test cases or hints");
      return;
    }
    try {
      await api.updateChallenge(c.id, {
        title: c.title, description: c.description, difficulty: c.difficulty,
        starter_code: c.starter_code, solution_code: c.solution_code,
        test_cases: tc, hints: hn, order: c.order,
      });
      setMsg("Saved ✓");
      setTimeout(() => setMsg(null), 1500);
    } catch (e) {
      setMsg(e instanceof Error ? e.message : "Failed");
    }
  };

  return (
    <div className="rounded-xl border bg-white p-4">
      <div className="mb-2 flex gap-2">
        <input value={c.title} onChange={(e) => setC({ ...c, title: e.target.value })}
          className="flex-1 rounded-md border p-2 text-sm font-medium" />
        <select value={c.difficulty} onChange={(e) => setC({ ...c, difficulty: e.target.value })}
          className="rounded-md border p-2 text-sm">
          <option value="easy">easy</option>
          <option value="medium">medium</option>
          <option value="hard">hard</option>
        </select>
      </div>
      <textarea value={c.description} onChange={(e) => setC({ ...c, description: e.target.value })}
        placeholder="Description" className="mb-2 h-16 w-full rounded-md border p-2 text-xs" />
      <div className="grid gap-2 md:grid-cols-2">
        <textarea value={c.starter_code} onChange={(e) => setC({ ...c, starter_code: e.target.value })}
          placeholder="starter_code" className="h-24 w-full rounded-md border bg-gray-900 p-2 font-mono text-xs text-gray-100" />
        <textarea value={c.solution_code} onChange={(e) => setC({ ...c, solution_code: e.target.value })}
          placeholder="solution_code" className="h-24 w-full rounded-md border bg-gray-900 p-2 font-mono text-xs text-gray-100" />
        <textarea value={testCases} onChange={(e) => setTestCases(e.target.value)}
          placeholder='test_cases JSON' className="h-24 w-full rounded-md border p-2 font-mono text-xs" />
        <textarea value={hints} onChange={(e) => setHints(e.target.value)}
          placeholder="hints JSON" className="h-24 w-full rounded-md border p-2 font-mono text-xs" />
      </div>
      <div className="mt-2 flex items-center gap-3 text-sm">
        <button onClick={save} className="rounded-md bg-brand-600 px-4 py-1.5 font-medium text-white hover:bg-brand-700">Save</button>
        <button onClick={async () => { if (confirm("Delete this challenge?")) { await api.deleteChallenge(c.id); onChanged(); } }}
          className="text-red-600 hover:underline">Delete</button>
        {msg && <span className={msg.includes("✓") ? "text-green-600" : "text-red-600"}>{msg}</span>}
      </div>
    </div>
  );
}

function QuizEditor({ question, onChanged }: { question: QuizQuestion; onChanged: () => void }) {
  const [q, setQ] = useState(question);
  const [options, setOptions] = useState(jsonText(question.options));
  const [msg, setMsg] = useState<string | null>(null);

  const save = async () => {
    let opts: unknown;
    try {
      opts = JSON.parse(options);
    } catch {
      setMsg("Invalid JSON in options");
      return;
    }
    try {
      await api.updateQuiz(q.id, {
        type: q.type, text: q.text, options: opts,
        correct_answer: q.correct_answer, explanation: q.explanation, order: q.order,
      });
      setMsg("Saved ✓");
      setTimeout(() => setMsg(null), 1500);
    } catch (e) {
      setMsg(e instanceof Error ? e.message : "Failed");
    }
  };

  return (
    <div className="rounded-xl border bg-white p-4">
      <div className="mb-2 flex gap-2">
        <select value={q.type} onChange={(e) => setQ({ ...q, type: e.target.value })}
          className="rounded-md border p-2 text-sm">
          <option value="multiple-choice">multiple-choice</option>
          <option value="fill-blank">fill-blank</option>
        </select>
        <input value={q.text} onChange={(e) => setQ({ ...q, text: e.target.value })}
          placeholder="Question text" className="flex-1 rounded-md border p-2 text-sm" />
      </div>
      <div className="grid gap-2 md:grid-cols-2">
        <textarea value={options} onChange={(e) => setOptions(e.target.value)}
          placeholder='options JSON (["A","B"]) — empty [] for fill-blank'
          className="h-20 w-full rounded-md border p-2 font-mono text-xs" />
        <div className="space-y-2">
          <input value={q.correct_answer} onChange={(e) => setQ({ ...q, correct_answer: e.target.value })}
            placeholder="correct_answer" className="w-full rounded-md border p-2 text-sm" />
          <input value={q.explanation} onChange={(e) => setQ({ ...q, explanation: e.target.value })}
            placeholder="explanation" className="w-full rounded-md border p-2 text-sm" />
        </div>
      </div>
      <div className="mt-2 flex items-center gap-3 text-sm">
        <button onClick={save} className="rounded-md bg-brand-600 px-4 py-1.5 font-medium text-white hover:bg-brand-700">Save</button>
        <button onClick={async () => { if (confirm("Delete this question?")) { await api.deleteQuiz(q.id); onChanged(); } }}
          className="text-red-600 hover:underline">Delete</button>
        {msg && <span className={msg.includes("✓") ? "text-green-600" : "text-red-600"}>{msg}</span>}
      </div>
    </div>
  );
}
