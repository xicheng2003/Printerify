import './assets/main.css'
import './assets/tailwind.css' // <-- 在文件的最顶部添加这一行
import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import { useUserStore } from '@/stores/user'

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)

// 在应用挂载前初始化用户状态
const userStore = useUserStore()
await userStore.initializeStore()

app.mount('#app')
