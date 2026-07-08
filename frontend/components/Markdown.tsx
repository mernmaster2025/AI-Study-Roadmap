import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

/**
 * Shared Markdown renderer — GitHub-flavored Markdown with Tailwind Typography,
 * theme-aware via `dark:prose-invert`. Matches the admin panel's preview style.
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
      <ReactMarkdown remarkPlugins={[remarkGfm]}>{children}</ReactMarkdown>
    </div>
  );
}
