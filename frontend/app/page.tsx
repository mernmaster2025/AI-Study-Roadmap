import Link from "next/link";

const FEATURES = [
  { icon: "🐍", title: "Hands-on Python", body: "Write and run code in the browser against real test cases." },
  { icon: "🎯", title: "12-Phase Roadmap", body: "From Python fundamentals all the way to production AI." },
  { icon: "📈", title: "Track Progress", body: "See challenges solved and phase completion at a glance." },
];

export default function Home() {
  return (
    <div>
      <section className="py-16 text-center">
        <h1 className="text-4xl font-extrabold tracking-tight sm:text-5xl">
          Learn AI, one runnable lesson at a time
        </h1>
        <p className="mx-auto mt-4 max-w-2xl text-lg text-gray-600">
          A 12-phase roadmap from Python fundamentals to production AI. Read,
          code, run, and get graded instantly.
        </p>
        <div className="mt-8 flex justify-center gap-4">
          <Link
            href="/dashboard"
            className="rounded-lg bg-brand-600 px-6 py-3 font-medium text-white hover:bg-brand-700"
          >
            Start learning
          </Link>
        </div>
      </section>

      <section className="grid gap-6 sm:grid-cols-3">
        {FEATURES.map((f) => (
          <div key={f.title} className="rounded-xl border bg-white p-6">
            <div className="text-3xl">{f.icon}</div>
            <h3 className="mt-3 font-semibold">{f.title}</h3>
            <p className="mt-1 text-sm text-gray-600">{f.body}</p>
          </div>
        ))}
      </section>
    </div>
  );
}
