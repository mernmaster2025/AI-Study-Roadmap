"use client";

import { useEffect, useState } from "react";
import {
  Box,
  Chip,
  IconButton,
  Paper,
  Switch,
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
import DeleteIcon from "@mui/icons-material/DeleteOutlineRounded";
import SearchIcon from "@mui/icons-material/SearchRounded";
import Shell from "@/components/Shell";
import { api, type AdminUser } from "@/lib/api";
import { useAuth } from "@/lib/auth";

export default function UsersPage() {
  return (
    <Shell>
      <Users />
    </Shell>
  );
}

function Users() {
  const { user: me } = useAuth();
  const [users, setUsers] = useState<AdminUser[]>([]);
  const [q, setQ] = useState("");

  const load = (query = "") =>
    api.users(query).then(setUsers).catch((e) => alert(e.message));
  useEffect(() => {
    load();
  }, []);

  const toggleAdmin = async (u: AdminUser) => {
    try {
      const updated = await api.updateUser(u.id, { is_admin: !u.is_admin });
      setUsers((p) => p.map((x) => (x.id === u.id ? updated : x)));
    } catch (e) {
      alert(e instanceof Error ? e.message : "Failed");
    }
  };

  const remove = async (u: AdminUser) => {
    if (!confirm(`Delete ${u.email}? Removes their submissions and progress too.`)) return;
    try {
      await api.deleteUser(u.id);
      setUsers((p) => p.filter((x) => x.id !== u.id));
    } catch (e) {
      alert(e instanceof Error ? e.message : "Failed");
    }
  };

  return (
    <Box>
      <Typography variant="h4" sx={{ mb: 2 }}>
        Users
      </Typography>
      <Box
        component="form"
        onSubmit={(e) => {
          e.preventDefault();
          load(q);
        }}
        sx={{ mb: 2, display: "flex", gap: 1 }}
      >
        <TextField
          size="small"
          placeholder="Search email or name…"
          value={q}
          onChange={(e) => setQ(e.target.value)}
          InputProps={{ startAdornment: <SearchIcon sx={{ mr: 1, color: "text.disabled" }} /> }}
          sx={{ width: 320 }}
        />
      </Box>

      <TableContainer component={Paper} variant="outlined">
        <Table size="small">
          <TableHead>
            <TableRow>
              <TableCell>Email</TableCell>
              <TableCell>Name</TableCell>
              <TableCell>Login</TableCell>
              <TableCell>Admin</TableCell>
              <TableCell>Joined</TableCell>
              <TableCell align="right" />
            </TableRow>
          </TableHead>
          <TableBody>
            {users.map((u) => (
              <TableRow key={u.id} hover>
                <TableCell sx={{ fontWeight: 600 }}>{u.email}</TableCell>
                <TableCell>{u.name}</TableCell>
                <TableCell>
                  <Chip
                    size="small"
                    label={u.has_password ? "password" : "oauth/dev"}
                    variant="outlined"
                  />
                </TableCell>
                <TableCell>
                  <Switch
                    checked={u.is_admin}
                    onChange={() => toggleAdmin(u)}
                    disabled={u.id === me?.id}
                    size="small"
                  />
                </TableCell>
                <TableCell sx={{ color: "text.secondary" }}>
                  {new Date(u.created_at).toLocaleDateString()}
                </TableCell>
                <TableCell align="right">
                  <Tooltip title={u.id === me?.id ? "You can't delete yourself" : "Delete"}>
                    <span>
                      <IconButton
                        size="small"
                        color="error"
                        disabled={u.id === me?.id}
                        onClick={() => remove(u)}
                      >
                        <DeleteIcon fontSize="small" />
                      </IconButton>
                    </span>
                  </Tooltip>
                </TableCell>
              </TableRow>
            ))}
            {users.length === 0 && (
              <TableRow>
                <TableCell colSpan={6} align="center" sx={{ py: 5, color: "text.secondary" }}>
                  No users found.
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  );
}
