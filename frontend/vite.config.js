// frontend/vite.config.js
import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [
    vue(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  // --- 添加下面的 server 配置 ---
  server: {
    proxy: {
      // 字符串简写写法
      // '/api': 'http://127.0.0.1:8000',

      // 选项写法，更灵活
      '/api': {
        target: 'http://127.0.0.1:8000', // 目标后端服务地址
        changeOrigin: true, // 需要虚拟主机站点
        // rewrite: (path) => path.replace(/^\/api/, '') // 如果后端接口没有/api前缀，需要重写路径
      },
      // 代理 /media 路径，以便能显示上传的图片等
      '/media': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      }
    }
  }
})
