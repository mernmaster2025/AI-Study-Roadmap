"use client";

import { useEffect, useState } from "react";
import {
  Box,
  Button,
  Chip,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  IconButton,
  MenuItem,
  Paper,
  Stack,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TextField,
  Tooltip,
  Typography,
} from "@mui/material";
import AddIcon from "@mui/icons-material/AddRounded";
import EditIcon from "@mui/icons-material/EditRounded";
import DeleteIcon from "@mui/icons-material/DeleteOutlineRounded";
import Shell from "@/components/Shell";
import MarkdownEditor from "@/components/MarkdownEditor";
import { api, type ChallengeListItem, type LessonListItem } from "@/lib/api";

export default function ChallengesPage() {
  return (
    <Shell>
      <Challenges />
    </Shell>
  );
}

const DIFF_COLOR: Record<string, "success" | "warning" | "error"> = {
  easy: "success", medium: "warning", hard: "error",
};

type Draft = {
  id?: string;
  lesson_id: string;
  title: string;
  description: string;
  difficulty: string;
  starter_code: string;
  solution_code: string;
  testCases: string;
  hints: string;
  order: number;
};

function code(sx = {}) {
  return {
    fontFamily: "ui-monospace, SFMono-Regular, Menlo, monospace",
    fontSize: 12,
    ...sx,
  };
}

function Challenges() {
  const [lessons, setLessons] = useState<LessonListItem[]>([]);
  const [items, setItems] = useState<ChallengeListItem[]>([]);
  const [filter, setFilter] = useState("");
  const [draft, setDraft] = useState<Draft | null>(null);
  const [saving, setSaving] = useState(false);

  const loadItems = (lessonId: string) =>
    api.allChallenges(lessonId || undefined).then(setItems).catch((e) => alert(e.message));

  useEffect(() => {
    api.allLessons().then(setLessons);
    loadItems("");
  }, []);

  const lessonLabel = (l: LessonListItem) => `P${l.phase_number} · ${l.title}`;

  const openNew = () =>
    setDraft({
      lesson_id: filter || lessons[0]?.id || "", title: "New challenge", description: "",
      difficulty: "easy", starter_code: "def solve():\n    pass\n", solution_code: "",
      testCases: "[]", hints: "[]", order: items.length,
    });

  const openEdit = async (item: ChallengeListItem) => {
    const c = await api.challenge(item.id);
    setDraft({
      id: c.id, lesson_id: c.lesson_id, title: c.title, description: c.description,
      difficulty: c.difficulty, starter_code: c.starter_code, solution_code: c.solution_code,
      testCases: JSON.stringify(c.test_cases, null, 2), hints: JSON.stringify(c.hints, null, 2),
      order: c.order,
    });
  };

  const save = async () => {
    if (!draft) return;
    let test_cases: unknown, hints: unknown;
    try {
      test_cases = JSON.parse(draft.testCases);
      hints = JSON.parse(draft.hints);
    } catch {
      alert("Invalid JSON in test cases or hints");
      return;
    }
    setSaving(true);
    try {
      const body = {
        title: draft.title, description: draft.description, difficulty: draft.difficulty,
        starter_code: draft.starter_code, solution_code: draft.solution_code,
        test_cases, hints, order: draft.order,
      };
      if (draft.id) await api.updateChallenge(draft.id, body);
      else await api.createChallenge({ lesson_id: draft.lesson_id, ...body });
      setDraft(null);
      loadItems(filter);
    } catch (e) {
      alert(e instanceof Error ? e.message : "Failed");
    } finally {
      setSaving(false);
    }
  };

  const remove = async (c: ChallengeListItem) => {
    if (!confirm(`Delete challenge "${c.title}"?`)) return;
    try {
      await api.deleteChallenge(c.id);
      setItems((p) => p.filter((x) => x.id !== c.id));
    } catch (e) {
      alert(e instanceof Error ? e.message : "Failed");
    }
  };

  return (
    <Box>
      <Stack direction="row" alignItems="center" justifyContent="space-between" sx={{ mb: 2 }}>
        <Typography variant="h4">Challenges</Typography>
        <Stack direction="row" spacing={2}>
          <TextField select size="small" label="Lesson" value={filter}
            onChange={(e) => { setFilter(e.target.value); loadItems(e.target.value); }} sx={{ width: 280 }}>
            <MenuItem value="">All lessons</MenuItem>
            {lessons.map((l) => (
              <MenuItem key={l.id} value={l.id}>{lessonLabel(l)}</MenuItem>
            ))}
          </TextField>
          <Button variant="contained" startIcon={<AddIcon />} onClick={openNew} disabled={!lessons.length}>
            Add challenge
          </Button>
        </Stack>
      </Stack>

      <TableContainer component={Paper} variant="outlined">
        <Table size="small">
          <TableHead>
            <TableRow>
              <TableCell>Lesson</TableCell>
              <TableCell>Title</TableCell>
              <TableCell>Difficulty</TableCell>
              <TableCell align="right" />
            </TableRow>
          </TableHead>
          <TableBody>
            {items.map((c) => (
              <TableRow key={c.id} hover>
                <TableCell sx={{ color: "text.secondary" }}>{c.lesson_title}</TableCell>
                <TableCell sx={{ fontWeight: 600 }}>{c.title}</TableCell>
                <TableCell>
                  <Chip size="small" label={c.difficulty} color={DIFF_COLOR[c.difficulty] ?? "default"} variant="outlined" />
                </TableCell>
                <TableCell align="right">
                  <Tooltip title="Edit">
                    <IconButton size="small" onClick={() => openEdit(c)}><EditIcon fontSize="small" /></IconButton>
                  </Tooltip>
                  <Tooltip title="Delete">
                    <IconButton size="small" color="error" onClick={() => remove(c)}><DeleteIcon fontSize="small" /></IconButton>
                  </Tooltip>
                </TableCell>
              </TableRow>
            ))}
            {items.length === 0 && (
              <TableRow><TableCell colSpan={4} align="center" sx={{ py: 5, color: "text.secondary" }}>No challenges.</TableCell></TableRow>
            )}
          </TableBody>
        </Table>
      </TableContainer>

      <Dialog open={!!draft} onClose={() => setDraft(null)} maxWidth="md" fullWidth>
        <DialogTitle>{draft?.id ? "Edit challenge" : "New challenge"}</DialogTitle>
        <DialogContent dividers>
          {draft && (
            <Stack spacing={2} sx={{ pt: 1 }}>
              <Stack direction="row" spacing={2}>
                {!draft.id && (
                  <TextField select label="Lesson" sx={{ width: 280 }} value={draft.lesson_id}
                    onChange={(e) => setDraft({ ...draft, lesson_id: e.target.value })}>
                    {lessons.map((l) => (<MenuItem key={l.id} value={l.id}>{lessonLabel(l)}</MenuItem>))}
                  </TextField>
                )}
                <TextField label="Title" fullWidth value={draft.title}
                  onChange={(e) => setDraft({ ...draft, title: e.target.value })} />
                <TextField select label="Difficulty" sx={{ width: 140 }} value={draft.difficulty}
                  onChange={(e) => setDraft({ ...draft, difficulty: e.target.value })}>
                  {["easy", "medium", "hard"].map((d) => (<MenuItem key={d} value={d}>{d}</MenuItem>))}
                </TextField>
              </Stack>
              <Box>
                <Typography variant="caption" color="text.secondary">Description (Markdown)</Typography>
                <MarkdownEditor value={draft.description} onChange={(v) => setDraft({ ...draft, description: v })} minHeight={120} />
              </Box>
              <Stack direction={{ xs: "column", md: "row" }} spacing={2}>
                <TextField label="Starter code" multiline minRows={5} fullWidth value={draft.starter_code}
                  onChange={(e) => setDraft({ ...draft, starter_code: e.target.value })} InputProps={{ sx: code() }} />
                <TextField label="Solution code" multiline minRows={5} fullWidth value={draft.solution_code}
                  onChange={(e) => setDraft({ ...draft, solution_code: e.target.value })} InputProps={{ sx: code() }} />
              </Stack>
              <Stack direction={{ xs: "column", md: "row" }} spacing={2}>
                <TextField label="Test cases (JSON)" multiline minRows={4} fullWidth value={draft.testCases}
                  onChange={(e) => setDraft({ ...draft, testCases: e.target.value })} InputProps={{ sx: code() }} />
                <TextField label="Hints (JSON)" multiline minRows={4} fullWidth value={draft.hints}
                  onChange={(e) => setDraft({ ...draft, hints: e.target.value })} InputProps={{ sx: code() }} />
              </Stack>
            </Stack>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDraft(null)}>Cancel</Button>
          <Button variant="contained" onClick={save} disabled={saving}>{saving ? "Saving…" : "Save"}</Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}
