import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],

  // Automatically start browser
  open: true,
  
  // Bind to all addresses:
  server: {
    host: true,
    port: 3000,
  },
})