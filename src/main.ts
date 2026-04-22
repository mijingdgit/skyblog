import { createApp } from 'vue'
import 'highlight.js/styles/atom-one-dark.css'
import router from './router'
import App from './App.vue'
import './style.css'

const app = createApp(App)
app.use(router)
app.mount('#app')

// Keep the current visual theme stable during the refactor.
document.documentElement.classList.add('dark')
