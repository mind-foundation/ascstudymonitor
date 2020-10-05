import qs from 'qs'
import VueRouter from 'vue-router'
import List from '@/views/List.vue'
import Single from '@/views/Single.vue'
import Queue from '@/views/Queue.vue'
import ListHero from '@/components/ListHero.vue'

const routes = [
  {
    path: '/p/:slug',
    name: 'Single',
    components: { main: Single },
    props: { main: true },
  },
  {
    path: '/queue/:channel',
    name: 'Queue',
    components: { main: Queue },
    props: { main: true },
  },
  {
    path: '*',
    name: 'List',
    components: {
      hero: ListHero,
      main: List,
    },
  },
]

const router = new VueRouter({
  mode: 'history',
  routes,
  parseQuery(query) {
    return qs.parse(query)
  },
  stringifyQuery(query) {
    var result = qs.stringify(query, { encode: false })

    return result ? '?' + result : ''
  },
})

export default router
