// frontend/vite.config.js
import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import os from 'node:os' // 导入Node.js的os模块

/**
 * 获取本机在局域网中的IPv4地址
 * @returns {string} 本机IP地址
 */
function getNetworkIp() {
  let needHost = ''; // 存储IP地址
  try {
    // 获取所有网络接口
    const networkInterfaces = os.networkInterfaces();

    for (const interfaceName in networkInterfaces) {
      const aInterface = networkInterfaces[interfaceName];
      for (let i = 0; i < aInterface.length; i++) {
        const aFace = aInterface[i];
        // 确保是IPv4地址，并且不是内部回环地址
        if (aFace.family === 'IPv4' && !aFace.internal) {
          needHost = aFace.address;
          break; // 找到第一个符合条件的即可
        }
      }
      if (needHost) break;
    }
  } catch (e) {
    needHost = 'localhost'; // 如果获取失败，则回退到localhost
  }
  return needHost;
}

const localIp = getNetworkIp();
const backendTarget = `http://${localIp}:8000`;

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
    host: true, // 这使得Vite监听所有地址，包括局域网地址
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
        // rewrite: (path) => path.replace(/^\/api/, '') // 如果后端接口没有/api前缀，需要重写路径
        // 【新增】在这里添加日志记录功能
        configure: (proxy, options) => {
          proxy.on('proxyReq', (proxyReq, req, res) => {
            console.log(`[VITE PROXY] [REQUEST] ${req.method} -> ${options.target}${proxyReq.path}`);
          });
          proxy.on('proxyRes', (proxyRes, req, res) => {
            console.log(`[VITE PROXY] [RESPONSE] ${req.method} ${req.url} -> ${proxyRes.statusCode}`);
          });
          proxy.on('error', (err, req, res) => {
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
  }
})
