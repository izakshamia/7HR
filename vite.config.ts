import path from "path"
import react from "@vitejs/plugin-react"
import { defineConfig } from "vite"

export default defineConfig({
  root: "./client",
  publicDir: "./public",
  build: {
    outDir: "dist",
    emptyOutDir: true,
    rollupOptions: {
      output: {
        entryFileNames: `assets/[name].js`,
        chunkFileNames: `assets/[name].js`,
        assetFileNames: `assets/[name].[ext]`
      }
    }
  },
  plugins: [react()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./client/src")
    }
  },
  server: {
    port: 3000,
    proxy: {
      '/api': 'http://127.0.0.1:5001',
      '/candidate': 'http://127.0.0.1:5001'
    }
  }
})