"use client";

import { useEffect, useState } from "react";
import {
  Box,
  Chip,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Typography,
} from "@mui/material";
import Shell from "@/components/Shell";
import { api, type Submission } from "@/lib/api";

export default function SubmissionsPage() {
  return (
    <Shell>
      <Submissions />
    </Shell>
  );
}

function Submissions() {
  const [rows, setRows] = useState<Submission[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    api.submissions(200).then(setRows).catch((e) => setError(e.message));
  }, []);

  return (
    <Box>
      <Typography variant="h4" sx={{ mb: 2 }}>
        Recent submissions
      </Typography>
      {error && <Typography color="error">{error}</Typography>}
      <TableContainer component={Paper} variant="outlined">
        <Table size="small">
          <TableHead>
            <TableRow>
              <TableCell>User</TableCell>
              <TableCell>Challenge</TableCell>
              <TableCell>Status</TableCell>
              <TableCell>Score</TableCell>
              <TableCell>Attempts</TableCell>
              <TableCell>When</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {rows.map((s) => (
              <TableRow key={s.id} hover>
                <TableCell>{s.user_email}</TableCell>
                <TableCell>{s.challenge_title}</TableCell>
                <TableCell>
                  <Chip
                    size="small"
                    label={s.status}
                    color={s.status === "passed" ? "success" : "error"}
                    variant={s.status === "passed" ? "filled" : "outlined"}
                  />
                </TableCell>
                <TableCell>{s.score}</TableCell>
                <TableCell>{s.attempts}</TableCell>
                <TableCell sx={{ color: "text.secondary" }}>
                  {new Date(s.submitted_at).toLocaleString()}
                </TableCell>
              </TableRow>
            ))}
            {rows.length === 0 && (
              <TableRow>
                <TableCell colSpan={6} align="center" sx={{ py: 5, color: "text.secondary" }}>
                  No submissions yet.
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  );
}
