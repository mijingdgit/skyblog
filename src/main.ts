import { createApp } from 'vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import 'element-plus/theme-chalk/dark/css-vars.css'
import 'highlight.js/styles/atom-one-dark.css'
import router from './router'
import App from './App.vue'
import './style.css'

const app = createApp(App)
app.use(ElementPlus)
app.use(router)
app.mount('#app')

// Keep the current visual theme stable during the refactor.
document.documentElement.classList.add('dark')
