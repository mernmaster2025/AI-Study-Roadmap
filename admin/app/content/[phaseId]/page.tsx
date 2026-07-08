"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import Shell from "@/components/Shell";
import { api, type Lesson, type Phase } from "@/lib/api";
import MarkdownEditor from "@/components/MarkdownEditor";

export default function PhaseAdminPage({
  params,
}: {
  params: { phaseId: string };
}) {
  return (
    <Shell>
      <PhaseAdmin phaseId={params.phaseId} />
    </Shell>
  );
}

function PhaseAdmin({ phaseId }: { phaseId: string }) {
  const [phase, setPhase] = useState<Phase | null>(null);
  const [lessons, setLessons] = useState<Lesson[]>([]);
  const [loading, setLoading] = useState(true);
  const [saved, setSaved] = useState(false);
  const [newTitle, setNewTitle] = useState("");

  const load = async () => {
    setLoading(true);
    const [phases, ls] = await Promise.all([api.phases(), api.lessons(phaseId)]);
    setPhase(phases.find((p) => p.id === phaseId) ?? null);
    setLessons(ls);
    setLoading(false);
  };
  useEffect(() => {
    load();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [phaseId]);

  const savePhase = async () => {
    if (!phase) return;
    await api.updatePhase(phase.id, {
      phase_number: phase.phase_number,
      title: phase.title,
      description: phase.description,
      estimated_hours: phase.estimated_hours,
      order: phase.order,
    });
    setSaved(true);
    setTimeout(() => setSaved(false), 1500);
  };

  const addLesson = async (e: React.FormEvent) => {
    e.preventDefault();
    await api.createLesson({
      phase_id: phaseId,
      lesson_number: lessons.length + 1,
      title: newTitle,
      order: lessons.length,
    });
    setNewTitle("");
    load();
  };

  const removeLesson = async (l: Lesson) => {
    if (!confirm(`Delete lesson "${l.title}" and its challenges/quiz?`)) return;
    await api.deleteLesson(l.id);
    setLessons((prev) => prev.filter((x) => x.id !== l.id));
  };

  if (loading) return <p className="text-gray-500">Loading…</p>;
  if (!phase) return <p>Phase not found.</p>;

  return (
    <div>
      <Link href="/content" className="text-sm text-brand-600 hover:underline">
        ← All phases
      </Link>

      <h1 className="mb-4 mt-2 text-2xl font-bold">Edit phase</h1>
      <div className="mb-8 space-y-3 rounded-xl border bg-white p-5">
        <div className="flex gap-3">
          <label className="w-28 text-sm">
            <span className="mb-1 block text-gray-500">Phase #</span>
            <input type="number" value={phase.phase_number}
              onChange={(e) => setPhase({ ...phase, phase_number: Number(e.target.value) })}
              className="w-full rounded-md border p-2" />
          </label>
          <label className="flex-1 text-sm">
            <span className="mb-1 block text-gray-500">Title</span>
            <input value={phase.title}
              onChange={(e) => setPhase({ ...phase, title: e.target.value })}
              className="w-full rounded-md border p-2" />
          </label>
          <label className="w-28 text-sm">
            <span className="mb-1 block text-gray-500">Hours</span>
            <input type="number" value={phase.estimated_hours}
              onChange={(e) => setPhase({ ...phase, estimated_hours: Number(e.target.value) })}
              className="w-full rounded-md border p-2" />
          </label>
        </div>
        <div className="text-sm">
          <span className="mb-1 block text-gray-500">Description (Markdown)</span>
          <MarkdownEditor
            value={phase.description}
            onChange={(v) => setPhase({ ...phase, description: v })}
            minHeight={200}
          />
        </div>
        <div className="flex items-center gap-3">
          <button onClick={savePhase}
            className="rounded-md bg-brand-600 px-5 py-2 text-sm font-medium text-white hover:bg-brand-700">
            Save phase
          </button>
          {saved && <span className="text-sm text-green-600">Saved ✓</span>}
        </div>
      </div>

      <div className="mb-3 flex items-center justify-between">
        <h2 className="text-xl font-bold">Lessons ({lessons.length})</h2>
      </div>
      <form onSubmit={addLesson} className="mb-4 flex gap-2">
        <input required value={newTitle} onChange={(e) => setNewTitle(e.target.value)}
          placeholder="New lesson title" className="flex-1 rounded-md border p-2 text-sm" />
        <button className="rounded-md border px-4 py-2 text-sm hover:bg-gray-50">+ Add lesson</button>
      </form>

      <div className="space-y-2">
        {lessons.map((l) => (
          <div key={l.id} className="flex items-center justify-between rounded-lg border bg-white p-4">
            <div>
              <span className="text-xs text-gray-400">#{l.lesson_number}</span>{" "}
              <span className="font-medium">{l.title}</span>
            </div>
            <div className="flex items-center gap-3 text-sm">
              <Link href={`/content/${phaseId}/${l.id}`} className="text-brand-600 hover:underline">
                Edit →
              </Link>
              <button onClick={() => removeLesson(l)} className="text-red-600 hover:underline">
                Delete
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
