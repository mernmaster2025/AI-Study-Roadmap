"use client";

import ReactMarkdown, { type Components } from "react-markdown";
import remarkGfm from "remark-gfm";
import { Highlight, themes } from "prism-react-renderer";

// Syntax-highlight fenced code blocks; leave inline code to the prose chip style.
const components: Components = {
  // react-markdown wraps block code in <pre><code>; we render our own <pre>,
  // so collapse the wrapper to avoid nesting.
  pre: ({ children }) => <>{children}</>,
  code({ className, children, ...props }) {
    const match = /language-(\w+)/.exec(className || "");
    const text = String(children).replace(/\n$/, "");
    if (!match) {
      return (
        <code className={className} {...props}>
          {children}
        </code>
      );
    }
    return (
      <Highlight theme={themes.vsDark} code={text} language={match[1]}>
        {({ style, tokens, getLineProps, getTokenProps }) => (
          <pre
            className="my-4 overflow-auto rounded-lg p-4 text-[13px] leading-relaxed"
            style={style}
          >
            {tokens.map((line, i) => (
              <div key={i} {...getLineProps({ line })}>
                {line.map((token, k) => (
                  <span key={k} {...getTokenProps({ token })} />
                ))}
              </div>
            ))}
          </pre>
        )}
      </Highlight>
    );
  },
};

/**
 * Shared Markdown renderer — GFM + Tailwind Typography (theme-aware via
 * `dark:prose-invert`) with syntax-highlighted code blocks.
 */
export default function Markdown({
  children,
  className = "",
}: {
  children: string;
  className?: string;
}) {
  return (
    <div className={`prose dark:prose-invert max-w-none ${className}`}>
      <ReactMarkdown remarkPlugins={[remarkGfm]} components={components}>
        {children}
      </ReactMarkdown>
    </div>
  );
}
