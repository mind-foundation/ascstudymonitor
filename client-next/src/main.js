import { createApp } from 'vue'
import App from './App.vue'
import './index.css'
import $events from './events'

const app = createApp(App)

app.provide($events, $events)

app.mount('#app')
