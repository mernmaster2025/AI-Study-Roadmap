"use client";

import {
  createContext,
  useContext,
  useEffect,
  useMemo,
  useState,
} from "react";
import {
  CssBaseline,
  ThemeProvider,
  createTheme,
  type PaletteMode,
} from "@mui/material";
import { AppRouterCacheProvider } from "@mui/material-nextjs/v14-appRouter";

const ThemeModeContext = createContext<{ mode: PaletteMode; toggle: () => void }>({
  mode: "dark",
  toggle: () => {},
});

export const useThemeMode = () => useContext(ThemeModeContext);

export function ThemeRegistry({ children }: { children: React.ReactNode }) {
  // Dark is the default.
  const [mode, setMode] = useState<PaletteMode>("dark");

  useEffect(() => {
    const saved = localStorage.getItem("admin_theme");
    if (saved === "light" || saved === "dark") setMode(saved);
  }, []);

  const toggle = () =>
    setMode((m) => {
      const next: PaletteMode = m === "dark" ? "light" : "dark";
      localStorage.setItem("admin_theme", next);
      return next;
    });

  const theme = useMemo(
    () =>
      createTheme({
        palette: {
          mode,
          primary: { main: "#7c8cff" },
          secondary: { main: "#22d3ee" },
          ...(mode === "dark"
            ? { background: { default: "#0b0f19", paper: "#131a2b" } }
            : { background: { default: "#f6f7fb", paper: "#ffffff" } }),
        },
        shape: { borderRadius: 12 },
        typography: {
          fontFamily:
            'system-ui, -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif',
          h4: { fontWeight: 700 },
          h5: { fontWeight: 700 },
          h6: { fontWeight: 700 },
        },
        components: {
          MuiButton: { defaultProps: { disableElevation: true } },
          MuiCard: {
            defaultProps: { elevation: 0 },
            styleOverrides: {
              root: {
                border: "1px solid",
                borderColor:
                  mode === "dark"
                    ? "rgba(255,255,255,0.08)"
                    : "rgba(0,0,0,0.08)",
                transition: "border-color .2s, transform .2s, box-shadow .2s",
              },
            },
          },
          MuiPaper: { styleOverrides: { root: { backgroundImage: "none" } } },
        },
      }),
    [mode]
  );

  return (
    <AppRouterCacheProvider options={{ key: "mui" }}>
      <ThemeModeContext.Provider value={{ mode, toggle }}>
        <ThemeProvider theme={theme}>
          <CssBaseline />
          {children}
        </ThemeProvider>
      </ThemeModeContext.Provider>
    </AppRouterCacheProvider>
  );
}
