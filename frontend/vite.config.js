import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// 使用固定的本地后端地址
const backendTarget = 'http://127.0.0.1:8000';

export default defineConfig({
  plugins: [
    vue(),
  ],
  resolve: {
    alias: {
      '@': new URL('./src', import.meta.url).pathname
    }
  },
  // --- 添加下面的 server 配置 ---
  server: {
    host: '127.0.0.1', // 只监听本地地址，不暴露到局域网
    proxy: {
      // 字符串简写写法
      // '/api': 'http://127.0.0.1:8000',

      // 将所有/api开头的请求代理到动态获取的后端地址
      '/api': {
        target: backendTarget, // 使用动态获取的后端地址
        // 如果后端接口需要跨域访问，可以设置以下选项
        // 这通常用于开发环境，生产环境可能不需要
        // 因为生产环境通常会将前后端部署在同一域名
        changeOrigin: true, // 需要虚拟主机站点
        // rewrite: (path) => path.replace(/^\\/api/, '') // 如果后端接口没有/api前缀，需要重写路径
        // 【新增】在这里添加日志记录功能
        configure: (proxy, options) => {
          proxy.on('proxyReq', (proxyReq, req) => {
            console.log(`[VITE PROXY] [REQUEST] ${req.method} -> ${options.target}${proxyReq.path}`);
          });
          proxy.on('proxyRes', (proxyRes, req) => {
            console.log(`[VITE PROXY] [RESPONSE] ${req.method} ${req.url} -> ${proxyRes.statusCode}`);
          });
          proxy.on('error', (err) => {
            console.error('[VITE PROXY] [ERROR]', err);
          });
        }

      },
      // 代理 /media 路径，以便能显示上传的图片等
      '/media': {
        target: backendTarget,
        changeOrigin: true,
      }
    }
  },
  // 测试配置
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: ['./src/test/setup.js'],
    include: ['**/*.{test,spec}.{js,mjs,cjs,ts,mts,cts,jsx,tsx}'],
    exclude: ['**/node_modules/**', '**/dist/**', '**/cypress/**'],
    coverage: {
      reporter: ['text', 'json', 'html'],
      exclude: [
        'node_modules/',
        'dist/',
        '**/*.d.ts',
        '**/setup.js',
        '**/main.js',
        '**/router/**',
        '**/App.vue'
      ]
    }
  }
})
