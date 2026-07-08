"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import Shell from "@/components/Shell";
import { api, type Phase } from "@/lib/api";

export default function ContentPage() {
  return (
    <Shell>
      <Content />
    </Shell>
  );
}

function Content() {
  const [phases, setPhases] = useState<Phase[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [adding, setAdding] = useState(false);
  const [form, setForm] = useState({ phase_number: "", title: "", estimated_hours: "" });

  const load = () => {
    setLoading(true);
    api.phases().then(setPhases).catch((e) => setError(e.message)).finally(() => setLoading(false));
  };
  useEffect(() => load(), []);

  const addPhase = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await api.createPhase({
        phase_number: Number(form.phase_number),
        title: form.title,
        estimated_hours: Number(form.estimated_hours || 0),
        order: phases.length,
      });
      setForm({ phase_number: "", title: "", estimated_hours: "" });
      setAdding(false);
      load();
    } catch (e) {
      alert(e instanceof Error ? e.message : "Failed");
    }
  };

  const remove = async (p: Phase) => {
    if (!confirm(`Delete phase "${p.title}" and ALL its lessons/challenges/quizzes?`)) return;
    try {
      await api.deletePhase(p.id);
      setPhases((prev) => prev.filter((x) => x.id !== p.id));
    } catch (e) {
      alert(e instanceof Error ? e.message : "Failed");
    }
  };

  return (
    <div>
      <div className="mb-4 flex items-center justify-between">
        <h1 className="text-2xl font-bold">Content · Phases</h1>
        <button
          onClick={() => setAdding((v) => !v)}
          className="rounded-md bg-brand-600 px-4 py-2 text-sm font-medium text-white hover:bg-brand-700"
        >
          {adding ? "Cancel" : "+ Add phase"}
        </button>
      </div>

      {adding && (
        <form onSubmit={addPhase} className="mb-4 flex flex-wrap gap-2 rounded-xl border bg-white p-4">
          <input required type="number" placeholder="Phase #" value={form.phase_number}
            onChange={(e) => setForm({ ...form, phase_number: e.target.value })}
            className="w-24 rounded-md border p-2 text-sm" />
          <input required placeholder="Title" value={form.title}
            onChange={(e) => setForm({ ...form, title: e.target.value })}
            className="flex-1 rounded-md border p-2 text-sm" />
          <input type="number" placeholder="Hours" value={form.estimated_hours}
            onChange={(e) => setForm({ ...form, estimated_hours: e.target.value })}
            className="w-24 rounded-md border p-2 text-sm" />
          <button className="rounded-md bg-brand-600 px-4 py-2 text-sm font-medium text-white">Create</button>
        </form>
      )}

      {error && <p className="text-red-600">{error}</p>}
      {loading ? (
        <p className="text-gray-500">Loading…</p>
      ) : (
        <div className="space-y-2">
          {phases.map((p) => (
            <div key={p.id} className="flex items-center justify-between rounded-xl border bg-white p-4">
              <div>
                <div className="text-xs font-medium uppercase tracking-wide text-brand-600">
                  Phase {p.phase_number} · {p.lesson_count} lessons · ~{p.estimated_hours}h
                </div>
                <div className="font-semibold">{p.title}</div>
              </div>
              <div className="flex items-center gap-3 text-sm">
                <Link href={`/content/${p.id}`} className="text-brand-600 hover:underline">
                  Manage →
                </Link>
                <button onClick={() => remove(p)} className="text-red-600 hover:underline">
                  Delete
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
