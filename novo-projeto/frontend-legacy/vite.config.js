import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: true, // Docker binding
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://backend:8000', // Nome do serviço no Docker Compose
        changeOrigin: true
      }
    }
  }
})
