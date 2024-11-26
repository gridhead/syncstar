import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      "/read": {
        target: "http://localhost:8080/read",
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/read/, ""),
      },
      "/sync": {
        target: "http://localhost:8080/sync",
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/sync/, ""),
      },
      "/sign": {
        target: "http://localhost:8080/sign",
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/sign/, ""),
      },
      "/exit": {
        target: "http://localhost:8080/exit",
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/exit/, ""),
      },
    },
  },
});
