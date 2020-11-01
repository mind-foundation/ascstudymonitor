import { createApp } from 'vue'
import App from './App.vue'
import $bus from './event.js'
import './index.css'

const app = createApp(App).mount('#app')
app.config.globalProperties.$events = $bus
