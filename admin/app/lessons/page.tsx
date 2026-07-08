"use client";

import { useEffect, useMemo, useState } from "react";
import {
  Box,
  Button,
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
import { api, type LessonListItem, type Phase } from "@/lib/api";

export default function LessonsPage() {
  return (
    <Shell>
      <Lessons />
    </Shell>
  );
}

type Draft = {
  id?: string;
  phase_id: string;
  lesson_number: number;
  title: string;
  estimated_minutes: number;
  order: number;
  description: string;
  content_markdown: string;
};

function Lessons() {
  const [phases, setPhases] = useState<Phase[]>([]);
  const [lessons, setLessons] = useState<LessonListItem[]>([]);
  const [filter, setFilter] = useState<string>("");
  const [draft, setDraft] = useState<Draft | null>(null);
  const [saving, setSaving] = useState(false);

  const loadLessons = (phaseId: string) =>
    api.allLessons(phaseId || undefined).then(setLessons).catch((e) => alert(e.message));

  useEffect(() => {
    // honor ?phase=<id> from the Phases page
    const initial = new URLSearchParams(window.location.search).get("phase") ?? "";
    setFilter(initial);
    api.phases().then(setPhases);
    loadLessons(initial);
  }, []);

  const changeFilter = (phaseId: string) => {
    setFilter(phaseId);
    loadLessons(phaseId);
  };

  const phaseName = useMemo(
    () => (id: string) => phases.find((p) => p.id === id)?.title ?? "",
    [phases]
  );

  const openNew = () => {
    const phase_id = filter || phases[0]?.id || "";
    const inPhase = lessons.filter((l) => l.phase_id === phase_id).length;
    setDraft({
      phase_id, lesson_number: inPhase + 1, title: "", estimated_minutes: 20,
      order: inPhase, description: "", content_markdown: "",
    });
  };

  const openEdit = async (item: LessonListItem) => {
    const full = await api.lesson(item.id);
    setDraft({
      id: full.id, phase_id: full.phase_id, lesson_number: full.lesson_number,
      title: full.title, estimated_minutes: full.estimated_minutes, order: full.order,
      description: full.description, content_markdown: full.content_markdown,
    });
  };

  const save = async () => {
    if (!draft) return;
    setSaving(true);
    try {
      if (draft.id) {
        await api.updateLesson(draft.id, {
          title: draft.title, description: draft.description,
          content_markdown: draft.content_markdown,
          estimated_minutes: draft.estimated_minutes, order: draft.order,
        });
      } else {
        await api.createLesson({
          phase_id: draft.phase_id, lesson_number: draft.lesson_number,
          title: draft.title, description: draft.description,
          content_markdown: draft.content_markdown,
          estimated_minutes: draft.estimated_minutes, order: draft.order,
        });
      }
      setDraft(null);
      loadLessons(filter);
    } catch (e) {
      alert(e instanceof Error ? e.message : "Failed");
    } finally {
      setSaving(false);
    }
  };

  const remove = async (l: LessonListItem) => {
    if (!confirm(`Delete lesson "${l.title}" and its challenges/quiz?`)) return;
    try {
      await api.deleteLesson(l.id);
      setLessons((p) => p.filter((x) => x.id !== l.id));
    } catch (e) {
      alert(e instanceof Error ? e.message : "Failed");
    }
  };

  return (
    <Box>
      <Stack direction="row" alignItems="center" justifyContent="space-between" sx={{ mb: 2 }}>
        <Typography variant="h4">Lessons</Typography>
        <Stack direction="row" spacing={2}>
          <TextField
            select size="small" label="Phase" value={filter}
            onChange={(e) => changeFilter(e.target.value)} sx={{ width: 240 }}
          >
            <MenuItem value="">All phases</MenuItem>
            {phases.map((p) => (
              <MenuItem key={p.id} value={p.id}>
                {p.phase_number}. {p.title}
              </MenuItem>
            ))}
          </TextField>
          <Button variant="contained" startIcon={<AddIcon />} onClick={openNew} disabled={!phases.length}>
            Add lesson
          </Button>
        </Stack>
      </Stack>

      <TableContainer component={Paper} variant="outlined">
        <Table size="small">
          <TableHead>
            <TableRow>
              <TableCell>Phase</TableCell>
              <TableCell width={50}>#</TableCell>
              <TableCell>Title</TableCell>
              <TableCell align="right" />
            </TableRow>
          </TableHead>
          <TableBody>
            {lessons.map((l) => (
              <TableRow key={l.id} hover>
                <TableCell sx={{ color: "text.secondary" }}>
                  {l.phase_number}. {l.phase_title}
                </TableCell>
                <TableCell>{l.lesson_number}</TableCell>
                <TableCell sx={{ fontWeight: 600 }}>{l.title}</TableCell>
                <TableCell align="right">
                  <Tooltip title="Edit">
                    <IconButton size="small" onClick={() => openEdit(l)}>
                      <EditIcon fontSize="small" />
                    </IconButton>
                  </Tooltip>
                  <Tooltip title="Delete">
                    <IconButton size="small" color="error" onClick={() => remove(l)}>
                      <DeleteIcon fontSize="small" />
                    </IconButton>
                  </Tooltip>
                </TableCell>
              </TableRow>
            ))}
            {lessons.length === 0 && (
              <TableRow>
                <TableCell colSpan={4} align="center" sx={{ py: 5, color: "text.secondary" }}>
                  No lessons.
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </TableContainer>

      <Dialog open={!!draft} onClose={() => setDraft(null)} maxWidth="md" fullWidth>
        <DialogTitle>{draft?.id ? "Edit lesson" : "New lesson"}</DialogTitle>
        <DialogContent dividers>
          {draft && (
            <Stack spacing={2} sx={{ pt: 1 }}>
              <Stack direction="row" spacing={2}>
                {!draft.id && (
                  <TextField
                    select label="Phase" sx={{ width: 220 }} value={draft.phase_id}
                    onChange={(e) => setDraft({ ...draft, phase_id: e.target.value })}
                  >
                    {phases.map((p) => (
                      <MenuItem key={p.id} value={p.id}>{p.phase_number}. {p.title}</MenuItem>
                    ))}
                  </TextField>
                )}
                <TextField
                  label="Minutes" type="number" sx={{ width: 120 }} value={draft.estimated_minutes}
                  onChange={(e) => setDraft({ ...draft, estimated_minutes: Number(e.target.value) })}
                />
                <TextField
                  label="Order" type="number" sx={{ width: 110 }} value={draft.order}
                  onChange={(e) => setDraft({ ...draft, order: Number(e.target.value) })}
                />
              </Stack>
              <TextField label="Title" fullWidth value={draft.title}
                onChange={(e) => setDraft({ ...draft, title: e.target.value })} />
              <Box>
                <Typography variant="caption" color="text.secondary">Description (beginner intro, Markdown)</Typography>
                <MarkdownEditor value={draft.description} onChange={(v) => setDraft({ ...draft, description: v })} minHeight={160} />
              </Box>
              <Box>
                <Typography variant="caption" color="text.secondary">Content (deep dive, Markdown)</Typography>
                <MarkdownEditor value={draft.content_markdown} onChange={(v) => setDraft({ ...draft, content_markdown: v })} minHeight={280} />
              </Box>
            </Stack>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDraft(null)}>Cancel</Button>
          <Button variant="contained" onClick={save} disabled={saving || !draft?.title}>
            {saving ? "Saving…" : "Save"}
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}
