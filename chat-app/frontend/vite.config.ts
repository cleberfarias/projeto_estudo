import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vuetify from 'vite-plugin-vuetify'
import { fileURLToPath, URL } from 'node:url'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    vuetify({ autoImport: true })
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  css: {
    preprocessorOptions: {
      scss: {
        additionalData: '@use "@/design-system/styles/mixins" as mixins;\n'
      }
    }
  },
  test: {
    globals: true,
    environment: 'jsdom',
    css: {
      modules: {
        classNameStrategy: 'non-scoped'
      }
    },
    setupFiles: ['./src/__tests__/setup.ts']
  }
})
