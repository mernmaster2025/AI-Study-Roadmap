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
import { api, type LessonListItem, type QuizListItem } from "@/lib/api";

export default function QuizzesPage() {
  return (
    <Shell>
      <Quizzes />
    </Shell>
  );
}

type Draft = {
  id?: string;
  lesson_id: string;
  type: string;
  text: string;
  options: string;
  correct_answer: string;
  explanation: string;
  order: number;
};

function Quizzes() {
  const [lessons, setLessons] = useState<LessonListItem[]>([]);
  const [items, setItems] = useState<QuizListItem[]>([]);
  const [filter, setFilter] = useState("");
  const [draft, setDraft] = useState<Draft | null>(null);
  const [saving, setSaving] = useState(false);

  const loadItems = (lessonId: string) =>
    api.allQuiz(lessonId || undefined).then(setItems).catch((e) => alert(e.message));

  useEffect(() => {
    api.allLessons().then(setLessons);
    loadItems("");
  }, []);

  const lessonLabel = (l: LessonListItem) => `P${l.phase_number} · ${l.title}`;

  const openNew = () =>
    setDraft({
      lesson_id: filter || lessons[0]?.id || "", type: "multiple-choice", text: "New question",
      options: JSON.stringify(["A", "B"], null, 2), correct_answer: "A", explanation: "", order: items.length,
    });

  const openEdit = async (item: QuizListItem) => {
    const q = await api.quizQuestion(item.id);
    setDraft({
      id: q.id, lesson_id: q.lesson_id, type: q.type, text: q.text,
      options: JSON.stringify(q.options, null, 2), correct_answer: q.correct_answer,
      explanation: q.explanation, order: q.order,
    });
  };

  const save = async () => {
    if (!draft) return;
    let options: unknown;
    try {
      options = JSON.parse(draft.options);
    } catch {
      alert("Invalid JSON in options");
      return;
    }
    setSaving(true);
    try {
      const body = {
        type: draft.type, text: draft.text, options,
        correct_answer: draft.correct_answer, explanation: draft.explanation, order: draft.order,
      };
      if (draft.id) await api.updateQuiz(draft.id, body);
      else await api.createQuiz({ lesson_id: draft.lesson_id, ...body });
      setDraft(null);
      loadItems(filter);
    } catch (e) {
      alert(e instanceof Error ? e.message : "Failed");
    } finally {
      setSaving(false);
    }
  };

  const remove = async (q: QuizListItem) => {
    if (!confirm("Delete this question?")) return;
    try {
      await api.deleteQuiz(q.id);
      setItems((p) => p.filter((x) => x.id !== q.id));
    } catch (e) {
      alert(e instanceof Error ? e.message : "Failed");
    }
  };

  return (
    <Box>
      <Stack direction="row" alignItems="center" justifyContent="space-between" sx={{ mb: 2 }}>
        <Typography variant="h4">Quiz questions</Typography>
        <Stack direction="row" spacing={2}>
          <TextField select size="small" label="Lesson" value={filter}
            onChange={(e) => { setFilter(e.target.value); loadItems(e.target.value); }} sx={{ width: 280 }}>
            <MenuItem value="">All lessons</MenuItem>
            {lessons.map((l) => (<MenuItem key={l.id} value={l.id}>{lessonLabel(l)}</MenuItem>))}
          </TextField>
          <Button variant="contained" startIcon={<AddIcon />} onClick={openNew} disabled={!lessons.length}>
            Add question
          </Button>
        </Stack>
      </Stack>

      <TableContainer component={Paper} variant="outlined">
        <Table size="small">
          <TableHead>
            <TableRow>
              <TableCell>Lesson</TableCell>
              <TableCell>Type</TableCell>
              <TableCell>Question</TableCell>
              <TableCell align="right" />
            </TableRow>
          </TableHead>
          <TableBody>
            {items.map((q) => (
              <TableRow key={q.id} hover>
                <TableCell sx={{ color: "text.secondary" }}>{q.lesson_title}</TableCell>
                <TableCell><Chip size="small" label={q.type} variant="outlined" /></TableCell>
                <TableCell>{q.text}</TableCell>
                <TableCell align="right">
                  <Tooltip title="Edit">
                    <IconButton size="small" onClick={() => openEdit(q)}><EditIcon fontSize="small" /></IconButton>
                  </Tooltip>
                  <Tooltip title="Delete">
                    <IconButton size="small" color="error" onClick={() => remove(q)}><DeleteIcon fontSize="small" /></IconButton>
                  </Tooltip>
                </TableCell>
              </TableRow>
            ))}
            {items.length === 0 && (
              <TableRow><TableCell colSpan={4} align="center" sx={{ py: 5, color: "text.secondary" }}>No questions.</TableCell></TableRow>
            )}
          </TableBody>
        </Table>
      </TableContainer>

      <Dialog open={!!draft} onClose={() => setDraft(null)} maxWidth="sm" fullWidth>
        <DialogTitle>{draft?.id ? "Edit question" : "New question"}</DialogTitle>
        <DialogContent dividers>
          {draft && (
            <Stack spacing={2} sx={{ pt: 1 }}>
              <Stack direction="row" spacing={2}>
                {!draft.id && (
                  <TextField select label="Lesson" sx={{ width: 240 }} value={draft.lesson_id}
                    onChange={(e) => setDraft({ ...draft, lesson_id: e.target.value })}>
                    {lessons.map((l) => (<MenuItem key={l.id} value={l.id}>{lessonLabel(l)}</MenuItem>))}
                  </TextField>
                )}
                <TextField select label="Type" sx={{ width: 180 }} value={draft.type}
                  onChange={(e) => setDraft({ ...draft, type: e.target.value })}>
                  <MenuItem value="multiple-choice">multiple-choice</MenuItem>
                  <MenuItem value="fill-blank">fill-blank</MenuItem>
                </TextField>
              </Stack>
              <TextField label="Question text" fullWidth multiline value={draft.text}
                onChange={(e) => setDraft({ ...draft, text: e.target.value })} />
              <TextField label='Options (JSON, e.g. ["A","B"]; [] for fill-blank)' fullWidth multiline minRows={3}
                value={draft.options} onChange={(e) => setDraft({ ...draft, options: e.target.value })}
                InputProps={{ sx: { fontFamily: "ui-monospace, monospace", fontSize: 12 } }} />
              <TextField label="Correct answer" fullWidth value={draft.correct_answer}
                onChange={(e) => setDraft({ ...draft, correct_answer: e.target.value })} />
              <TextField label="Explanation" fullWidth multiline value={draft.explanation}
                onChange={(e) => setDraft({ ...draft, explanation: e.target.value })} />
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
