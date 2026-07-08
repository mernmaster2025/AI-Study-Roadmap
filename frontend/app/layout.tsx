import type { Metadata } from "next";
import "./globals.css";
import { AuthProvider } from "@/lib/auth";
import { ThemeProvider } from "@/lib/theme";
import Navbar from "@/components/Navbar";

export const metadata: Metadata = {
  title: "AI Study Platform",
  description: "Learn AI from Python fundamentals to production — hands-on.",
};

// Applied before paint so dark (the default) never flashes light on first load.
const noFlash = `
try {
  var t = localStorage.getItem('theme');
  if (t === 'light') document.documentElement.classList.remove('dark');
  else document.documentElement.classList.add('dark');
} catch (e) { document.documentElement.classList.add('dark'); }
`;

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark" suppressHydrationWarning>
      <head>
        <script dangerouslySetInnerHTML={{ __html: noFlash }} />
      </head>
      <body>
        <ThemeProvider>
          <AuthProvider>
            <Navbar />
            <main className="mx-auto max-w-6xl px-6 py-8">{children}</main>
          </AuthProvider>
        </ThemeProvider>
      </body>
    </html>
  );
}
