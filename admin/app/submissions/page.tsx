"use client";

import { useEffect, useState } from "react";
import Shell from "@/components/Shell";
import { api, type Submission } from "@/lib/api";

export default function SubmissionsPage() {
  return (
    <Shell>
      <Submissions />
    </Shell>
  );
}

function Submissions() {
  const [rows, setRows] = useState<Submission[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    api
      .submissions(200)
      .then(setRows)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, []);

  return (
    <div>
      <h1 className="mb-4 text-2xl font-bold">Recent submissions</h1>
      {error && <p className="text-red-600">{error}</p>}
      {loading ? (
        <p className="text-gray-500">Loading…</p>
      ) : (
        <div className="overflow-x-auto rounded-xl border bg-white">
          <table className="w-full text-sm">
            <thead className="border-b bg-gray-50 text-left text-gray-500">
              <tr>
                <th className="p-3">User</th>
                <th className="p-3">Challenge</th>
                <th className="p-3">Status</th>
                <th className="p-3">Score</th>
                <th className="p-3">Attempts</th>
                <th className="p-3">When</th>
              </tr>
            </thead>
            <tbody>
              {rows.map((s) => (
                <tr key={s.id} className="border-b last:border-0">
                  <td className="p-3">{s.user_email}</td>
                  <td className="p-3">{s.challenge_title}</td>
                  <td className="p-3">
                    <span
                      className={`rounded-full px-2 py-0.5 text-xs font-medium ${
                        s.status === "passed"
                          ? "bg-green-100 text-green-700"
                          : "bg-red-100 text-red-700"
                      }`}
                    >
                      {s.status}
                    </span>
                  </td>
                  <td className="p-3">{s.score}</td>
                  <td className="p-3">{s.attempts}</td>
                  <td className="p-3 text-gray-500">
                    {new Date(s.submitted_at).toLocaleString()}
                  </td>
                </tr>
              ))}
              {rows.length === 0 && (
                <tr>
                  <td colSpan={6} className="p-6 text-center text-gray-500">
                    No submissions yet.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
