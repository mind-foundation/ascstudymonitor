import qs from 'qs'
import Vue from 'vue'
import VueRouter from 'vue-router'
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
  parseQuery: qs.parse,
  stringifyQuery: function(query) {
    const result = qs.stringify(query)
    return result ? '?' + result : ''
  },
})

export default router
