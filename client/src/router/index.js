// import qs from 'qs'
import VueRouter from 'vue-router'
import List from '@/views/List.vue'
import Single from '@/views/Single.vue'
import Queue from '@/views/Queue.vue'
import ListHero from '@/components/ListHero.vue'

const routes = [
  {
    path: window.urlForPublication,
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
  base: process.env.BASE_URL,
  routes,
  // parseQuery(query) {
  //   const parsed = qs.parse(query)

  //   // put the + back in search
  //   if (parsed.search) {
  //     parsed.search = parsed.search.replace(/\s/g, '+')
  //   }
  //   return parsed
  // },
  // stringifyQuery(query) {
  //   // remove empty strings
  //   for (const k in query) {
  //     if (query[k] === '') {
  //       delete query[k]
  //     }
  //   }

  //   return qs.stringify(query, {
  //     encode: false,
  //     addQueryPrefix: true,
  //   })
  // },
})

export default router
