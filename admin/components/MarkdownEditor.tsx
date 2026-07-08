"use client";

import { useRef, useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

interface Props {
  value: string;
  onChange: (value: string) => void;
  minHeight?: number;
  placeholder?: string;
}

type Tab = "write" | "preview";

/**
 * A lightweight GitHub-style Markdown editor: a formatting toolbar over a
 * textarea, plus a Write/Preview tab toggle that renders GFM Markdown.
 */
export default function MarkdownEditor({
  value,
  onChange,
  minHeight = 240,
  placeholder = "Write Markdown…",
}: Props) {
  const ref = useRef<HTMLTextAreaElement>(null);
  const [tab, setTab] = useState<Tab>("write");

  // Wrap the current selection with `before`/`after` (e.g. **bold**).
  const surround = (before: string, after = before, ph = "text") => {
    const ta = ref.current;
    if (!ta) return;
    const { selectionStart: s, selectionEnd: e } = ta;
    const selected = value.slice(s, e) || ph;
    const next = value.slice(0, s) + before + selected + after + value.slice(e);
    onChange(next);
    requestAnimationFrame(() => {
      ta.focus();
      ta.selectionStart = s + before.length;
      ta.selectionEnd = s + before.length + selected.length;
    });
  };

  // Prefix each selected line (headings, quotes, list items).
  const prefixLines = (prefix: string, numbered = false) => {
    const ta = ref.current;
    if (!ta) return;
    const { selectionStart: s, selectionEnd: e } = ta;
    const lineStart = value.lastIndexOf("\n", s - 1) + 1;
    const block = value.slice(lineStart, e) || "";
    const prefixed = block
      .split("\n")
      .map((l, i) => (numbered ? `${i + 1}. ` : prefix) + l)
      .join("\n");
    const next = value.slice(0, lineStart) + prefixed + value.slice(e);
    onChange(next);
    requestAnimationFrame(() => ta.focus());
  };

  const insertBlock = (text: string) => {
    const ta = ref.current;
    if (!ta) return;
    const { selectionStart: s } = ta;
    const next = value.slice(0, s) + text + value.slice(s);
    onChange(next);
    requestAnimationFrame(() => {
      ta.focus();
      ta.selectionStart = ta.selectionEnd = s + text.length;
    });
  };

  const TOOLS: { label: string; title: string; run: () => void }[] = [
    { label: "H1", title: "Heading 1", run: () => prefixLines("# ") },
    { label: "H2", title: "Heading 2", run: () => prefixLines("## ") },
    { label: "B", title: "Bold", run: () => surround("**") },
    { label: "I", title: "Italic", run: () => surround("_") },
    { label: "“ ”", title: "Quote", run: () => prefixLines("> ") },
    { label: "•", title: "Bullet list", run: () => prefixLines("- ") },
    { label: "1.", title: "Numbered list", run: () => prefixLines("", true) },
    { label: "<>", title: "Inline code", run: () => surround("`") },
    { label: "{ }", title: "Code block", run: () => insertBlock("\n```python\n\n```\n") },
    { label: "🔗", title: "Link", run: () => surround("[", "](https://)", "text") },
  ];

  return (
    <div className="overflow-hidden rounded-md border">
      {/* Tabs + toolbar */}
      <div className="flex items-center gap-1 border-b bg-gray-50 px-2 py-1">
        <button
          type="button"
          onClick={() => setTab("write")}
          className={`rounded px-3 py-1 text-sm ${
            tab === "write" ? "bg-white font-medium shadow-sm" : "text-gray-500"
          }`}
        >
          Write
        </button>
        <button
          type="button"
          onClick={() => setTab("preview")}
          className={`rounded px-3 py-1 text-sm ${
            tab === "preview" ? "bg-white font-medium shadow-sm" : "text-gray-500"
          }`}
        >
          Preview
        </button>

        {tab === "write" && (
          <div className="ml-2 flex flex-wrap items-center gap-0.5 border-l pl-2">
            {TOOLS.map((t) => (
              <button
                key={t.label}
                type="button"
                title={t.title}
                onClick={t.run}
                className="rounded px-2 py-1 text-xs text-gray-600 hover:bg-gray-200"
              >
                {t.label}
              </button>
            ))}
          </div>
        )}
      </div>

      {tab === "write" ? (
        <textarea
          ref={ref}
          value={value}
          onChange={(e) => onChange(e.target.value)}
          placeholder={placeholder}
          spellCheck={false}
          style={{ minHeight }}
          className="w-full resize-y bg-white p-3 font-mono text-xs outline-none"
        />
      ) : (
        <div
          style={{ minHeight }}
          className="prose prose-sm max-w-none overflow-auto bg-white p-4"
        >
          {value.trim() ? (
            <ReactMarkdown remarkPlugins={[remarkGfm]}>{value}</ReactMarkdown>
          ) : (
            <p className="text-gray-400">Nothing to preview.</p>
          )}
        </div>
      )}
    </div>
  );
}
