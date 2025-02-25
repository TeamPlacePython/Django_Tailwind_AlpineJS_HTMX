import { defineConfig } from 'vite'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
    plugins: [
      tailwindcss(),
    ],
    base: "/static/",
    build: {
      manifest: "manifest.json",
      outDir: "./static",
      emptyOutDir: true,
      rollupOptions: {
        input: {
          styles: "./src/css/styles.css"
        }
      },
    },
  });