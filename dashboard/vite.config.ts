import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// GitHub Pages project site needs a subpath; local/Vercel stay at "/"
const base = process.env.GITHUB_PAGES === "true" ? "/sybil-sweep/" : "/";

export default defineConfig({
  base,
  plugins: [react()],
  server: {
    port: 5173,
    open: true,
  },
});
