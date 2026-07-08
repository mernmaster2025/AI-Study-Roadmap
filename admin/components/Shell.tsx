"use client";

import { useEffect } from "react";
import { useRouter, usePathname } from "next/navigation";
import NextLink from "next/link";
import {
  AppBar,
  Box,
  CircularProgress,
  Divider,
  Drawer,
  IconButton,
  List,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Toolbar,
  Tooltip,
  Typography,
} from "@mui/material";
import DashboardIcon from "@mui/icons-material/SpaceDashboardRounded";
import LayersIcon from "@mui/icons-material/LayersRounded";
import MenuBookIcon from "@mui/icons-material/MenuBookRounded";
import CodeIcon from "@mui/icons-material/CodeRounded";
import QuizIcon from "@mui/icons-material/QuizRounded";
import PeopleIcon from "@mui/icons-material/PeopleAltRounded";
import AssignmentIcon from "@mui/icons-material/AssignmentTurnedInRounded";
import LightModeIcon from "@mui/icons-material/LightModeRounded";
import DarkModeIcon from "@mui/icons-material/DarkModeRounded";
import LogoutIcon from "@mui/icons-material/LogoutRounded";
import { useAuth } from "@/lib/auth";
import { useThemeMode } from "@/lib/theme";

const DRAWER_WIDTH = 232;

const NAV = [
  { href: "/", label: "Dashboard", icon: <DashboardIcon /> },
  { href: "/phases", label: "Phases", icon: <LayersIcon /> },
  { href: "/lessons", label: "Lessons", icon: <MenuBookIcon /> },
  { href: "/challenges", label: "Challenges", icon: <CodeIcon /> },
  { href: "/quizzes", label: "Quizzes", icon: <QuizIcon /> },
  { href: "/users", label: "Users", icon: <PeopleIcon /> },
  { href: "/submissions", label: "Submissions", icon: <AssignmentIcon /> },
];

export default function Shell({ children }: { children: React.ReactNode }) {
  const { user, loading, logout } = useAuth();
  const { mode, toggle } = useThemeMode();
  const router = useRouter();
  const pathname = usePathname();

  useEffect(() => {
    if (!loading && !user) router.replace("/login");
  }, [loading, user, router]);

  if (loading)
    return (
      <Box sx={{ display: "grid", placeItems: "center", height: "100vh" }}>
        <CircularProgress />
      </Box>
    );
  if (!user) return null;

  const isActive = (href: string) =>
    href === "/" ? pathname === "/" : pathname.startsWith(href);

  return (
    <Box sx={{ display: "flex" }}>
      <AppBar
        position="fixed"
        color="default"
        elevation={0}
        sx={{
          zIndex: (t) => t.zIndex.drawer + 1,
          borderBottom: "1px solid",
          borderColor: "divider",
          backdropFilter: "blur(8px)",
          backgroundColor: (t) =>
            t.palette.mode === "dark"
              ? "rgba(19,26,43,0.7)"
              : "rgba(255,255,255,0.7)",
        }}
      >
        <Toolbar sx={{ gap: 1 }}>
          <Typography variant="h6" sx={{ flexGrow: 1, fontWeight: 800 }}>
            <Box component="span" sx={{ color: "primary.main" }}>
              AI Study
            </Box>{" "}
            Admin
          </Typography>
          <Tooltip title={mode === "dark" ? "Light mode" : "Dark mode"}>
            <IconButton onClick={toggle} color="inherit">
              {mode === "dark" ? <LightModeIcon /> : <DarkModeIcon />}
            </IconButton>
          </Tooltip>
          <Typography variant="body2" sx={{ color: "text.secondary", mx: 1 }}>
            {user.email}
          </Typography>
          <Tooltip title="Sign out">
            <IconButton onClick={logout} color="inherit">
              <LogoutIcon />
            </IconButton>
          </Tooltip>
        </Toolbar>
      </AppBar>

      <Drawer
        variant="permanent"
        sx={{
          width: DRAWER_WIDTH,
          flexShrink: 0,
          "& .MuiDrawer-paper": {
            width: DRAWER_WIDTH,
            boxSizing: "border-box",
            borderRight: "1px solid",
            borderColor: "divider",
          },
        }}
      >
        <Toolbar />
        <List sx={{ px: 1.2, py: 1 }}>
          {NAV.map((n) => {
            const active = isActive(n.href);
            return (
              <ListItemButton
                key={n.href}
                component={NextLink}
                href={n.href}
                selected={active}
                sx={{
                  borderRadius: 2,
                  mb: 0.5,
                  transition: "background-color .2s, transform .15s",
                  "&:hover": { transform: "translateX(2px)" },
                  "&.Mui-selected": {
                    bgcolor: "primary.main",
                    color: "primary.contrastText",
                    "& .MuiListItemIcon-root": { color: "primary.contrastText" },
                    "&:hover": { bgcolor: "primary.main" },
                  },
                }}
              >
                <ListItemIcon sx={{ minWidth: 40 }}>{n.icon}</ListItemIcon>
                <ListItemText primaryTypographyProps={{ fontSize: 14, fontWeight: 600 }}>
                  {n.label}
                </ListItemText>
              </ListItemButton>
            );
          })}
        </List>
        <Divider />
      </Drawer>

      <Box component="main" sx={{ flexGrow: 1, minWidth: 0, p: 3 }}>
        <Toolbar />
        <Box sx={{ maxWidth: 1100, mx: "auto" }}>{children}</Box>
      </Box>
    </Box>
  );
}
