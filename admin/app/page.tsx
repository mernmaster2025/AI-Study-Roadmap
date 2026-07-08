"use client";

import { useEffect, useState } from "react";
import {
  Box,
  Card,
  CardContent,
  Grow,
  Typography,
} from "@mui/material";
import PeopleIcon from "@mui/icons-material/PeopleAltRounded";
import ShieldIcon from "@mui/icons-material/ShieldRounded";
import LayersIcon from "@mui/icons-material/LayersRounded";
import MenuBookIcon from "@mui/icons-material/MenuBookRounded";
import CodeIcon from "@mui/icons-material/CodeRounded";
import QuizIcon from "@mui/icons-material/QuizRounded";
import AssignmentIcon from "@mui/icons-material/AssignmentRounded";
import CheckCircleIcon from "@mui/icons-material/CheckCircleRounded";
import PsychologyIcon from "@mui/icons-material/PsychologyRounded";
import Shell from "@/components/Shell";
import { api, type Stats } from "@/lib/api";

export default function DashboardPage() {
  return (
    <Shell>
      <Dashboard />
    </Shell>
  );
}

function Dashboard() {
  const [stats, setStats] = useState<Stats | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    api.stats().then(setStats).catch((e) => setError(e.message));
  }, []);

  if (error) return <Typography color="error">{error}</Typography>;
  if (!stats) return <Typography color="text.secondary">Loading…</Typography>;

  const cards = [
    { label: "Users", value: stats.users, icon: <PeopleIcon />, color: "#7c8cff" },
    { label: "Admins", value: stats.admins, icon: <ShieldIcon />, color: "#f59e0b" },
    { label: "Phases", value: stats.phases, icon: <LayersIcon />, color: "#22d3ee" },
    { label: "Lessons", value: stats.lessons, icon: <MenuBookIcon />, color: "#34d399" },
    { label: "Challenges", value: stats.challenges, icon: <CodeIcon />, color: "#f472b6" },
    { label: "Quiz questions", value: stats.quiz_questions, icon: <QuizIcon />, color: "#a78bfa" },
    { label: "Submissions", value: stats.submissions, icon: <AssignmentIcon />, color: "#60a5fa" },
    { label: "Passed", value: stats.passed_submissions, icon: <CheckCircleIcon />, color: "#4ade80" },
    { label: "Quiz attempts", value: stats.quiz_attempts, icon: <PsychologyIcon />, color: "#fb7185" },
  ];

  return (
    <Box>
      <Typography variant="h4" sx={{ mb: 3 }}>
        Dashboard
      </Typography>
      <Box
        sx={{
          display: "grid",
          gap: 2,
          gridTemplateColumns: {
            xs: "repeat(2, 1fr)",
            sm: "repeat(3, 1fr)",
          },
        }}
      >
        {cards.map((c, i) => (
          <Grow in timeout={300 + i * 90} key={c.label}>
            <Card
              sx={{
                "&:hover": { transform: "translateY(-3px)", boxShadow: 6 },
              }}
            >
              <CardContent>
                <Box
                  sx={{
                    width: 44,
                    height: 44,
                    borderRadius: 2,
                    display: "grid",
                    placeItems: "center",
                    color: c.color,
                    bgcolor: `${c.color}22`,
                  }}
                >
                  {c.icon}
                </Box>
                <Typography variant="h4" sx={{ mt: 1.5 }}>
                  {c.value.toLocaleString()}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  {c.label}
                </Typography>
              </CardContent>
            </Card>
          </Grow>
        ))}
      </Box>
    </Box>
  );
}
