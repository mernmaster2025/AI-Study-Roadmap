"use client";

import { useRef, useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import {
  Box,
  Divider,
  IconButton,
  Paper,
  TextField,
  ToggleButton,
  ToggleButtonGroup,
  Tooltip,
} from "@mui/material";
import FormatBoldIcon from "@mui/icons-material/FormatBold";
import FormatItalicIcon from "@mui/icons-material/FormatItalic";
import FormatQuoteIcon from "@mui/icons-material/FormatQuote";
import FormatListBulletedIcon from "@mui/icons-material/FormatListBulleted";
import FormatListNumberedIcon from "@mui/icons-material/FormatListNumbered";
import CodeIcon from "@mui/icons-material/Code";
import DataObjectIcon from "@mui/icons-material/DataObject";
import LinkIcon from "@mui/icons-material/Link";

interface Props {
  value: string;
  onChange: (value: string) => void;
  minHeight?: number;
  placeholder?: string;
}

export default function MarkdownEditor({
  value,
  onChange,
  minHeight = 220,
  placeholder = "Write Markdown…",
}: Props) {
  const ref = useRef<HTMLTextAreaElement>(null);
  const [tab, setTab] = useState<"write" | "preview">("write");

  const surround = (before: string, after = before, ph = "text") => {
    const ta = ref.current;
    if (!ta) return;
    const { selectionStart: s, selectionEnd: e } = ta;
    const selected = value.slice(s, e) || ph;
    onChange(value.slice(0, s) + before + selected + after + value.slice(e));
    requestAnimationFrame(() => {
      ta.focus();
      ta.selectionStart = s + before.length;
      ta.selectionEnd = s + before.length + selected.length;
    });
  };

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
    onChange(value.slice(0, lineStart) + prefixed + value.slice(e));
    requestAnimationFrame(() => ta.focus());
  };

  const insertBlock = (text: string) => {
    const ta = ref.current;
    if (!ta) return;
    const { selectionStart: s } = ta;
    onChange(value.slice(0, s) + text + value.slice(s));
    requestAnimationFrame(() => {
      ta.focus();
      ta.selectionStart = ta.selectionEnd = s + text.length;
    });
  };

  const tools = [
    { title: "Heading 1", label: "H1", run: () => prefixLines("# ") },
    { title: "Heading 2", label: "H2", run: () => prefixLines("## ") },
    { title: "Bold", icon: <FormatBoldIcon fontSize="small" />, run: () => surround("**") },
    { title: "Italic", icon: <FormatItalicIcon fontSize="small" />, run: () => surround("_") },
    { title: "Quote", icon: <FormatQuoteIcon fontSize="small" />, run: () => prefixLines("> ") },
    { title: "Bullet list", icon: <FormatListBulletedIcon fontSize="small" />, run: () => prefixLines("- ") },
    { title: "Numbered list", icon: <FormatListNumberedIcon fontSize="small" />, run: () => prefixLines("", true) },
    { title: "Inline code", icon: <CodeIcon fontSize="small" />, run: () => surround("`") },
    { title: "Code block", icon: <DataObjectIcon fontSize="small" />, run: () => insertBlock("\n```python\n\n```\n") },
    { title: "Link", icon: <LinkIcon fontSize="small" />, run: () => surround("[", "](https://)", "text") },
  ];

  return (
    <Paper variant="outlined" sx={{ borderRadius: 2, overflow: "hidden" }}>
      <Box
        sx={{
          display: "flex",
          alignItems: "center",
          gap: 0.5,
          flexWrap: "wrap",
          px: 1,
          py: 0.5,
          bgcolor: "action.hover",
          borderBottom: "1px solid",
          borderColor: "divider",
        }}
      >
        <ToggleButtonGroup
          size="small"
          exclusive
          value={tab}
          onChange={(_, v) => v && setTab(v)}
          sx={{ "& .MuiToggleButton-root": { px: 1.5, py: 0.3, textTransform: "none" } }}
        >
          <ToggleButton value="write">Write</ToggleButton>
          <ToggleButton value="preview">Preview</ToggleButton>
        </ToggleButtonGroup>

        {tab === "write" && (
          <>
            <Divider orientation="vertical" flexItem sx={{ mx: 0.5 }} />
            {tools.map((t) => (
              <Tooltip key={t.title} title={t.title}>
                <IconButton size="small" onClick={t.run} sx={{ borderRadius: 1.5 }}>
                  {t.icon ?? (
                    <Box component="span" sx={{ fontSize: 12, fontWeight: 700 }}>
                      {t.label}
                    </Box>
                  )}
                </IconButton>
              </Tooltip>
            ))}
          </>
        )}
      </Box>

      {tab === "write" ? (
        <TextField
          inputRef={ref}
          value={value}
          onChange={(e) => onChange(e.target.value)}
          placeholder={placeholder}
          multiline
          fullWidth
          variant="standard"
          InputProps={{
            disableUnderline: true,
            sx: {
              p: 1.5,
              alignItems: "flex-start",
              fontFamily: "ui-monospace, SFMono-Regular, Menlo, monospace",
              fontSize: 13,
              "& textarea": { minHeight },
            },
          }}
        />
      ) : (
        <Box className="md-preview" sx={{ p: 2, minHeight, overflow: "auto" }}>
          {value.trim() ? (
            <ReactMarkdown remarkPlugins={[remarkGfm]}>{value}</ReactMarkdown>
          ) : (
            <Box sx={{ color: "text.disabled" }}>Nothing to preview.</Box>
          )}
        </Box>
      )}
    </Paper>
  );
}
