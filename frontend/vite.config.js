import { defineConfig } from 'vite';
import { resolve } from 'path';

export default defineConfig({
  base: '/static/dist/',
  build: {
    manifest: true,
    outDir: resolve(__dirname, '../static/dist'),
    rollupOptions: {
      input: resolve(__dirname, 'src/main.js'),
    },
  },
  server: {
    host: true,
    port: 5173,
    origin: 'http://localhost:5173',
  },
});
