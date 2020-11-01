import { createApp, h, provide } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import { DefaultApolloClient } from '@vue/apollo-composable'
import App from './App.vue'
import './index.css'
import $events from './events.ts'
import $filters from './filters.ts'
import { EventsSymbol, FiltersSymbol } from './symbols.ts'
import List from '/@/views/List.vue'
import ListHero from '/@/components/ListHero.vue'
import { apolloClient } from '/@/graphql.js'
// import { createProvider } from './vue-apollo.js'

const app = createApp({
  setup() {
    provide(DefaultApolloClient, apolloClient)
    provide(EventsSymbol, $events)
    provide(FiltersSymbol, $filters)
  },
  render: () => h(App),
})

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
      path: '/',
      name: 'list',
      components: {
        main: List,
        hero: ListHero,
      },
    },
  ],
})

app.use(router)

app.mount('#app')
