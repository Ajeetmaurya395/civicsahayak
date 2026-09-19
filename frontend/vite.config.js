import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [
    react(),
    tailwindcss(),
  ],
  server: {
    port: 3000,
    proxy: {
      '/chat': 'http://localhost:8000',
      '/profile': 'http://localhost:8000',
      '/schemes': 'http://localhost:8000',
      '/documents': 'http://localhost:8000',
      '/health': 'http://localhost:8000',
    },
  },
})
