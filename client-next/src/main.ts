import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'
import './index.css'
import $events from './events.js'
import List from '/@/views/List.vue'
import ListHero from '/@/components/ListHero.vue'

const app = createApp(App)

app.provide($events, $events)

const router = createRouter({
  history: createWebHistory(),
  routes: [
    //   {
    //   path: '/p/:slug',
    //   name: 'Single',
    //   components: { main: Single },
    //   props: { main: true },
    // },
    // {
    //   path: '/queue/:channel',
    //   name: 'Queue',
    //   components: { main: Queue },
    //   props: { main: true },
    // },
    {
      path: '/:pathMatch(.*)*',
      name: 'list',
      components: {
        hero: ListHero,
        main: List,
      },
    },
  ],
})

app.use(router)

app.mount('#app')
