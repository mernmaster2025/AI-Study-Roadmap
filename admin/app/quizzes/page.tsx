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
import QuizIcon from "@mui/icons-material/QuizRounded";
import Shell from "@/components/Shell";
import { api, type LessonListItem, type Phase, type QuizListItem } from "@/lib/api";

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
  const [phases, setPhases] = useState<Phase[]>([]);
  const [phaseId, setPhaseId] = useState("");
  const [lessons, setLessons] = useState<LessonListItem[]>([]);
  const [lessonId, setLessonId] = useState("");
  const [items, setItems] = useState<QuizListItem[]>([]);
  const [draft, setDraft] = useState<Draft | null>(null);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    api.phases().then(setPhases);
  }, []);

  const selectPhase = (pid: string) => {
    setPhaseId(pid);
    setLessonId("");
    setItems([]);
    setLessons([]);
    if (pid) api.allLessons(pid).then(setLessons).catch((e) => alert(e.message));
  };

  const selectLesson = (lid: string) => {
    setLessonId(lid);
    if (lid) api.allQuiz(lid).then(setItems).catch((e) => alert(e.message));
    else setItems([]);
  };

  const openNew = () => {
    if (!lessonId) return;
    setDraft({
      lesson_id: lessonId, type: "multiple-choice", text: "New question",
      options: JSON.stringify(["A", "B"], null, 2), correct_answer: "A", explanation: "", order: items.length,
    });
  };

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
      selectLesson(lessonId);
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
          <TextField select size="small" label="Phase" value={phaseId}
            onChange={(e) => selectPhase(e.target.value)} sx={{ width: 200 }}>
            {phases.map((p) => (<MenuItem key={p.id} value={p.id}>{p.phase_number}. {p.title}</MenuItem>))}
          </TextField>
          <TextField select size="small" label="Lesson" value={lessonId}
            onChange={(e) => selectLesson(e.target.value)} sx={{ width: 240 }} disabled={!phaseId}>
            {lessons.map((l) => (<MenuItem key={l.id} value={l.id}>{l.lesson_number}. {l.title}</MenuItem>))}
          </TextField>
          <Button variant="contained" startIcon={<AddIcon />} onClick={openNew} disabled={!lessonId}>
            Add
          </Button>
        </Stack>
      </Stack>

      {!lessonId ? (
        <Paper variant="outlined" sx={{ p: 6, textAlign: "center", color: "text.secondary" }}>
          <QuizIcon sx={{ fontSize: 40, opacity: 0.5 }} />
          <Typography sx={{ mt: 1 }}>
            {phaseId ? "Select a lesson to view its questions." : "Select a phase, then a lesson."}
          </Typography>
        </Paper>
      ) : (
        <TableContainer component={Paper} variant="outlined">
          <Table size="small">
            <TableHead>
              <TableRow>
                <TableCell width={160}>Type</TableCell>
                <TableCell>Question</TableCell>
                <TableCell align="right" />
              </TableRow>
            </TableHead>
            <TableBody>
              {items.map((q) => (
                <TableRow key={q.id} hover>
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
                <TableRow><TableCell colSpan={3} align="center" sx={{ py: 5, color: "text.secondary" }}>No questions in this lesson yet.</TableCell></TableRow>
              )}
            </TableBody>
          </Table>
        </TableContainer>
      )}

      <Dialog open={!!draft} onClose={() => setDraft(null)} maxWidth="sm" fullWidth>
        <DialogTitle>{draft?.id ? "Edit question" : "New question"}</DialogTitle>
        <DialogContent dividers>
          {draft && (
            <Stack spacing={2} sx={{ pt: 1 }}>
              <TextField select label="Type" sx={{ width: 200 }} value={draft.type}
                onChange={(e) => setDraft({ ...draft, type: e.target.value })}>
                <MenuItem value="multiple-choice">multiple-choice</MenuItem>
                <MenuItem value="fill-blank">fill-blank</MenuItem>
              </TextField>
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
