"use client";

import { useEffect, useState } from "react";
import NextLink from "next/link";
import {
  Box,
  Button,
  Chip,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  IconButton,
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
import { api, type Phase } from "@/lib/api";

export default function PhasesPage() {
  return (
    <Shell>
      <Phases />
    </Shell>
  );
}

type Draft = {
  id?: string;
  phase_number: number;
  title: string;
  estimated_hours: number;
  order: number;
  description: string;
};

function Phases() {
  const [phases, setPhases] = useState<Phase[]>([]);
  const [draft, setDraft] = useState<Draft | null>(null);
  const [saving, setSaving] = useState(false);

  const load = () => api.phases().then(setPhases).catch((e) => alert(e.message));
  useEffect(() => {
    load();
  }, []);

  const openNew = () =>
    setDraft({ phase_number: phases.length + 1, title: "", estimated_hours: 0, order: phases.length, description: "" });
  const openEdit = (p: Phase) =>
    setDraft({ id: p.id, phase_number: p.phase_number, title: p.title, estimated_hours: p.estimated_hours, order: p.order, description: p.description });

  const save = async () => {
    if (!draft) return;
    setSaving(true);
    try {
      const body = {
        phase_number: draft.phase_number, title: draft.title,
        estimated_hours: draft.estimated_hours, order: draft.order, description: draft.description,
      };
      if (draft.id) await api.updatePhase(draft.id, body);
      else await api.createPhase(body);
      setDraft(null);
      load();
    } catch (e) {
      alert(e instanceof Error ? e.message : "Failed");
    } finally {
      setSaving(false);
    }
  };

  const remove = async (p: Phase) => {
    if (!confirm(`Delete phase "${p.title}" and ALL its lessons/challenges/quizzes?`)) return;
    try {
      await api.deletePhase(p.id);
      setPhases((prev) => prev.filter((x) => x.id !== p.id));
    } catch (e) {
      alert(e instanceof Error ? e.message : "Failed");
    }
  };

  return (
    <Box>
      <Stack direction="row" alignItems="center" justifyContent="space-between" sx={{ mb: 2 }}>
        <Typography variant="h4">Phases</Typography>
        <Button variant="contained" startIcon={<AddIcon />} onClick={openNew}>
          Add phase
        </Button>
      </Stack>

      <TableContainer component={Paper} variant="outlined">
        <Table size="small">
          <TableHead>
            <TableRow>
              <TableCell width={70}>#</TableCell>
              <TableCell>Title</TableCell>
              <TableCell>Lessons</TableCell>
              <TableCell>Hours</TableCell>
              <TableCell align="right" />
            </TableRow>
          </TableHead>
          <TableBody>
            {phases.map((p) => (
              <TableRow key={p.id} hover>
                <TableCell>{p.phase_number}</TableCell>
                <TableCell sx={{ fontWeight: 600 }}>{p.title}</TableCell>
                <TableCell>
                  <Chip
                    size="small"
                    label={p.lesson_count}
                    component={NextLink}
                    href={`/lessons?phase=${p.id}`}
                    clickable
                  />
                </TableCell>
                <TableCell>~{p.estimated_hours}h</TableCell>
                <TableCell align="right">
                  <Tooltip title="Edit">
                    <IconButton size="small" onClick={() => openEdit(p)}>
                      <EditIcon fontSize="small" />
                    </IconButton>
                  </Tooltip>
                  <Tooltip title="Delete">
                    <IconButton size="small" color="error" onClick={() => remove(p)}>
                      <DeleteIcon fontSize="small" />
                    </IconButton>
                  </Tooltip>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>

      <Dialog open={!!draft} onClose={() => setDraft(null)} maxWidth="md" fullWidth>
        <DialogTitle>{draft?.id ? "Edit phase" : "New phase"}</DialogTitle>
        <DialogContent dividers>
          {draft && (
            <Stack spacing={2} sx={{ pt: 1 }}>
              <Stack direction="row" spacing={2}>
                <TextField
                  label="Phase #" type="number" sx={{ width: 120 }}
                  value={draft.phase_number}
                  onChange={(e) => setDraft({ ...draft, phase_number: Number(e.target.value) })}
                />
                <TextField
                  label="Title" fullWidth value={draft.title}
                  onChange={(e) => setDraft({ ...draft, title: e.target.value })}
                />
                <TextField
                  label="Hours" type="number" sx={{ width: 120 }}
                  value={draft.estimated_hours}
                  onChange={(e) => setDraft({ ...draft, estimated_hours: Number(e.target.value) })}
                />
              </Stack>
              <Box>
                <Typography variant="caption" color="text.secondary">Description (Markdown)</Typography>
                <MarkdownEditor value={draft.description} onChange={(v) => setDraft({ ...draft, description: v })} minHeight={220} />
              </Box>
            </Stack>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDraft(null)}>Cancel</Button>
          <Button variant="contained" onClick={save} disabled={saving}>
            {saving ? "Saving…" : "Save"}
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}
