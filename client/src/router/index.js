import Vue from 'vue'
import VueRouter from 'vue-router'
import qs from 'qs'

import List from '../views/List.vue'
import Publication from '../views/Publication.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: window.urlForPublication,
    name: 'Publication',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    // component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
    component: Publication,
    props: true,
  },
  {
    path: '*',
    name: 'List',
    component: List,
  },
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes,
  parseQuery(query) {
    const parsed = qs.parse(query)

    // put the + back in search
    if (parsed.search) {
      parsed.search = parsed.search.replace(/\s/g, '+')
    }
    return parsed
  },
  stringifyQuery(query) {
    // remove empty strings
    for (const k in query) {
      if (query[k] === '') {
        delete query[k]
      }
    }

    return qs.stringify(query, {
      encode: false,
      addQueryPrefix: true,
    })
  },
})

export default router
