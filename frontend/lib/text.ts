// Turn a Markdown string into a short plain-text teaser for cards/lists.
export function teaser(markdown: string, maxLen = 160): string {
  const plain = markdown
    .replace(/```[\s\S]*?```/g, " ") // fenced code
    .replace(/`([^`]+)`/g, "$1") // inline code
    .replace(/!\[[^\]]*\]\([^)]*\)/g, "") // images
    .replace(/\[([^\]]+)\]\([^)]*\)/g, "$1") // links -> text
    .replace(/^#{1,6}\s+/gm, "") // headings
    .replace(/[*_>#-]/g, " ") // md symbols
    .replace(/\s+/g, " ") // collapse whitespace
    .trim();
  return plain.length > maxLen ? plain.slice(0, maxLen).trimEnd() + "…" : plain;
}
