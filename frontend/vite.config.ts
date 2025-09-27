import { defineConfig } from 'vite'
import path from 'path'
import tailwindcss from '@tailwindcss/vite'
import react from '@vitejs/plugin-react'

/**
 * Vite configuration for the MyBrand Job Application Platform frontend
 * 
 * This configuration sets up the Vite build system with:
 * 1. Path aliases for easier imports
 * 2. Tailwind CSS integration for styling
 * 3. React plugin for JSX transformation
 * 4. Development mode optimizations
 */

export default defineConfig({
  /**
   * Path resolution configuration
   * 
   * Sets up aliases for common import paths:
   * - @/* maps to the root of the frontend directory
   * - ~backend/client maps to the client.ts file
   * - ~backend/* maps to the backend directory
   */
  resolve: {
    alias: {
      '@': path.resolve(__dirname),
      '~backend/client': path.resolve(__dirname, './client'),
      '~backend': path.resolve(__dirname, '../backend'),
    },
  },
  
  /**
   * Plugin configuration
   * 
   * Integrates essential plugins for the development environment:
   * - tailwindcss: Enables Tailwind CSS processing
   * - react: Enables React JSX transformation
   */
  plugins: [
    tailwindcss(),
    react(),
  ],
  
  /**
   * Development mode configuration
   * 
   * Sets the application to development mode and disables minification
   * for easier debugging during development.
   */
  mode: "development",
  build: {
    minify: false,
  }
})