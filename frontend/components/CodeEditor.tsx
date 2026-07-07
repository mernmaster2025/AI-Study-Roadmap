"use client";

import { useState } from "react";
import { Highlight, themes } from "prism-react-renderer";
import { api, type Challenge, type ExecuteResult } from "@/lib/api";
import { useAuth } from "@/lib/auth";

interface Props {
  challenge: Challenge;
  onSolved?: () => void;
}

export default function CodeEditor({ challenge, onSolved }: Props) {
  const { user, login } = useAuth();
  const [code, setCode] = useState(challenge.starter_code);
  const [result, setResult] = useState<ExecuteResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [hintsShown, setHintsShown] = useState(0);

  const run = async () => {
    setLoading(true);
    setError(null);
    try {
      if (!user) await login(); // auto sign-in the demo user on first run
      const res = await api.executeCode(challenge.id, code);
      setResult(res);
      if (res.all_tests_passed) onSolved?.();
    } catch (e) {
      setError(e instanceof Error ? e.message : "Something went wrong");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="grid gap-6 lg:grid-cols-2">
      {/* ---- Editor ---- */}
      <div>
        <div className="mb-2 flex items-center justify-between">
          <h3 className="font-semibold">Your Code</h3>
          <button
            onClick={() => setCode(challenge.starter_code)}
            className="text-xs text-gray-500 hover:text-gray-800"
          >
            Reset
          </button>
        </div>

        {/* Textarea + syntax-highlight overlay share the same box + metrics. */}
        <div className="relative h-96 overflow-auto rounded-lg bg-[#1e1e2e] font-mono text-sm">
          <Highlight theme={themes.vsDark} code={code} language="python">
            {({ tokens, getLineProps, getTokenProps }) => (
              <pre className="pointer-events-none absolute inset-0 m-0 overflow-hidden p-4 leading-6">
                {tokens.map((line, i) => (
                  <div key={i} {...getLineProps({ line })}>
                    {line.map((token, key) => (
                      <span key={key} {...getTokenProps({ token })} />
                    ))}
                  </div>
                ))}
              </pre>
            )}
          </Highlight>
          <textarea
            value={code}
            onChange={(e) => setCode(e.target.value)}
            spellCheck={false}
            className="absolute inset-0 h-full w-full resize-none overflow-hidden whitespace-pre bg-transparent p-4 leading-6 text-transparent caret-white outline-none"
          />
        </div>

        <div className="mt-3 flex items-center gap-3">
          <button
            onClick={run}
            disabled={loading}
            className="rounded-md bg-brand-600 px-5 py-2 font-medium text-white hover:bg-brand-700 disabled:opacity-50"
          >
            {loading ? "Running…" : "Run & Submit"}
          </button>
          {challenge.hints.length > 0 && hintsShown < challenge.hints.length && (
            <button
              onClick={() => setHintsShown((n) => n + 1)}
              className="rounded-md border px-4 py-2 text-sm hover:bg-gray-50"
            >
              Show hint ({hintsShown}/{challenge.hints.length})
            </button>
          )}
        </div>

        {hintsShown > 0 && (
          <ul className="mt-3 space-y-1 rounded-md bg-amber-50 p-3 text-sm text-amber-900">
            {challenge.hints.slice(0, hintsShown).map((h, i) => (
              <li key={i}>💡 {h}</li>
            ))}
          </ul>
        )}
      </div>

      {/* ---- Output / results ---- */}
      <div>
        <h3 className="mb-2 font-semibold">Output</h3>
        <pre className="h-24 overflow-auto rounded-lg bg-gray-100 p-3 text-sm">
          {error
            ? `Error: ${error}`
            : result?.error
              ? result.error
              : result?.output || "Run your code to see output."}
        </pre>

        <div className="mt-4">
          <div className="mb-2 flex items-center justify-between">
            <h3 className="font-semibold">Test Results</h3>
            {result && (
              <span
                className={
                  result.all_tests_passed
                    ? "text-sm font-medium text-green-600"
                    : "text-sm font-medium text-gray-500"
                }
              >
                {result.test_results.filter((t) => t.passed).length}/
                {result.test_results.length} passing
              </span>
            )}
          </div>

          {result?.all_tests_passed && (
            <div className="mb-3 rounded-md bg-green-100 p-3 text-sm font-medium text-green-800">
              🎉 All tests passed — challenge solved!
            </div>
          )}

          <div className="space-y-2">
            {(result?.test_results ?? []).map((t) => (
              <div
                key={t.test_number}
                className={`rounded-md p-3 text-sm ${
                  t.passed ? "bg-green-50" : "bg-red-50"
                }`}
              >
                <p className="font-medium">
                  Test {t.test_number}: {t.passed ? "✓ Passed" : "✗ Failed"}
                </p>
                {t.error ? (
                  <p className="mt-1 text-red-700">Error: {t.error}</p>
                ) : (
                  !t.passed && (
                    <p className="mt-1 text-gray-600">
                      Expected <code>{t.expected}</code>, got{" "}
                      <code>{t.actual}</code>
                    </p>
                  )
                )}
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
