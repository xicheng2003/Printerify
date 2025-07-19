import './assets/main.css'
import './assets/tailwind.css' // <-- 在文件的最顶部添加这一行
import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

const app = createApp(App)

app.use(createPinia())
app.use(router)

app.mount('#app')
