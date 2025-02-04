import { defineConfig } from 'vite'
import tailwindcss from '@tailwindcss/vite'
import { svelte } from '@sveltejs/vite-plugin-svelte'

// https://vite.dev/config/
export default defineConfig({
  plugins: [svelte(), tailwindcss()],
  server: {
    host: '0.0.0.0',
    port: 5173,
    // If your hosting environment needs to see the domain, also set allowedHosts
    allowedHosts: ['upload.w3d.box.ca'],
  fs: {
    allow: ['..']
  },
  // For HMR to use your domain + SSL:
  hmr: {
    protocol: 'wss',
    host: 'upload.w3d.box.ca',
    port: 5173  // If you're behind an HTTPS proxy, it’s often 443 externally
  }
 },
 assetsInclude: ['**/*.png', '**/*.wav', '**/*.ttf']
})
