import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { VitePWA } from 'vite-plugin-pwa';
import fs from 'fs';
import path from 'path';
import { fileURLToPath, pathToFileURL } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// A simple Vite plugin to run Vercel serverless functions locally
function vercelApiMock() {
  return {
    name: 'vercel-api-mock',
    configureServer(server) {
      server.middlewares.use('/api', (req, res, next) => {
        let body = '';
        req.on('data', chunk => { body += chunk.toString(); });
        req.on('end', async () => {
          if (body) {
            try { req.body = JSON.parse(body); } catch(e) {}
          } else {
            req.body = {};
          }
          
          // mock express-like res methods
          res.status = (code) => { res.statusCode = code; return res; };
          res.json = (data) => {
            res.setHeader('Content-Type', 'application/json');
            res.end(JSON.stringify(data));
          };

          try {
            const urlPath = req.url.split('?')[0]; // e.g. /connect
            const absolutePath = path.resolve(__dirname, `api${urlPath}.js`);
            console.log('API Request:', req.url, '-> absolutePath:', absolutePath, 'exists?', fs.existsSync(absolutePath));
            
            if (fs.existsSync(absolutePath)) {
              // Convert absolute path to a file URL to import it dynamically on Windows
              const fileUrl = pathToFileURL(absolutePath).href;
              const module = await import(`${fileUrl}?t=${Date.now()}`); // bust cache
              await module.default(req, res);
            } else {
              next();
            }
          } catch(e) {
            console.error('API Error:', e);
            res.status(500).json({ error: e.message });
          }
        });
      });
    }
  }
}

export default defineConfig({
  plugins: [
    react(),
    vercelApiMock(),
    VitePWA({
      registerType: 'autoUpdate',
      injectRegister: 'auto',
      devOptions: {
        enabled: true
      },
      workbox: {
        globPatterns: ['**/*.{js,css,html,ico,png,svg,json}'],
        maximumFileSizeToCacheInBytes: 5 * 1024 * 1024,
      },
      manifest: {
        name: 'Softly Built POS',
        short_name: 'SoftlyBuilt',
        description: 'Softly Built POS & Inventory Management System',
        theme_color: '#ffffff',
        background_color: '#ffffff',
        display: 'standalone'
      }
    })
  ],
  server: {
    port: 5173,
    open: true,
  },
  build: {
    outDir: 'dist',
    sourcemap: false,
    chunkSizeWarningLimit: 2000,
  },
});
