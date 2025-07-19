/** @type {import('tailwindcss').Config} */
export default {
  // 指定哪些文件将使用 Tailwind CSS
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
  },
  // 核心配置：禁用 Preflight (全局样式重置)
  // 这是确保不与您现有 CSS 冲突的关键！
  corePlugins: {
    preflight: false,
  },
  plugins: [],
}
