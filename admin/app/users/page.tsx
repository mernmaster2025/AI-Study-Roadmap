"use client";

import { useEffect, useState } from "react";
import Shell from "@/components/Shell";
import { api, type AdminUser } from "@/lib/api";
import { useAuth } from "@/lib/auth";

export default function UsersPage() {
  return (
    <Shell>
      <Users />
    </Shell>
  );
}

function Users() {
  const { user: me } = useAuth();
  const [users, setUsers] = useState<AdminUser[]>([]);
  const [q, setQ] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const load = (query = "") => {
    setLoading(true);
    api
      .users(query)
      .then(setUsers)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  };

  useEffect(() => load(), []);

  const toggleAdmin = async (u: AdminUser) => {
    try {
      const updated = await api.updateUser(u.id, { is_admin: !u.is_admin });
      setUsers((prev) => prev.map((x) => (x.id === u.id ? updated : x)));
    } catch (e) {
      alert(e instanceof Error ? e.message : "Failed");
    }
  };

  const remove = async (u: AdminUser) => {
    if (!confirm(`Delete ${u.email}? This also removes their submissions and progress.`))
      return;
    try {
      await api.deleteUser(u.id);
      setUsers((prev) => prev.filter((x) => x.id !== u.id));
    } catch (e) {
      alert(e instanceof Error ? e.message : "Failed");
    }
  };

  return (
    <div>
      <h1 className="mb-4 text-2xl font-bold">Users</h1>
      <form
        onSubmit={(e) => {
          e.preventDefault();
          load(q);
        }}
        className="mb-4 flex gap-2"
      >
        <input
          value={q}
          onChange={(e) => setQ(e.target.value)}
          placeholder="Search email or name…"
          className="w-72 rounded-md border p-2 text-sm"
        />
        <button className="rounded-md border px-4 py-2 text-sm hover:bg-gray-50">
          Search
        </button>
      </form>

      {error && <p className="text-red-600">{error}</p>}
      {loading ? (
        <p className="text-gray-500">Loading…</p>
      ) : (
        <div className="overflow-x-auto rounded-xl border bg-white">
          <table className="w-full text-sm">
            <thead className="border-b bg-gray-50 text-left text-gray-500">
              <tr>
                <th className="p-3">Email</th>
                <th className="p-3">Name</th>
                <th className="p-3">Login</th>
                <th className="p-3">Admin</th>
                <th className="p-3">Joined</th>
                <th className="p-3"></th>
              </tr>
            </thead>
            <tbody>
              {users.map((u) => (
                <tr key={u.id} className="border-b last:border-0">
                  <td className="p-3 font-medium">{u.email}</td>
                  <td className="p-3">{u.name}</td>
                  <td className="p-3 text-gray-500">
                    {u.has_password ? "password" : "oauth/dev"}
                  </td>
                  <td className="p-3">
                    <button
                      onClick={() => toggleAdmin(u)}
                      disabled={u.id === me?.id}
                      className={`rounded-full px-2.5 py-1 text-xs font-medium ${
                        u.is_admin
                          ? "bg-green-100 text-green-700"
                          : "bg-gray-100 text-gray-600"
                      } ${u.id === me?.id ? "opacity-50" : "hover:opacity-80"}`}
                      title={u.id === me?.id ? "You can't change your own role" : "Toggle admin"}
                    >
                      {u.is_admin ? "Admin" : "Learner"}
                    </button>
                  </td>
                  <td className="p-3 text-gray-500">
                    {new Date(u.created_at).toLocaleDateString()}
                  </td>
                  <td className="p-3 text-right">
                    {u.id !== me?.id && (
                      <button
                        onClick={() => remove(u)}
                        className="text-red-600 hover:underline"
                      >
                        Delete
                      </button>
                    )}
                  </td>
                </tr>
              ))}
              {users.length === 0 && (
                <tr>
                  <td colSpan={6} className="p-6 text-center text-gray-500">
                    No users found.
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
