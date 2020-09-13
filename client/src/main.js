import Vue from 'vue'
import VueSocialSharing from 'vue-social-sharing'
import { sync } from 'vuex-router-sync'
import VModal from 'vue-js-modal'
import VueClipboard from 'vue-clipboard2'
import Toasted from 'vue-toasted'
import VueHotkey from 'v-hotkey'
import * as Sentry from '@sentry/browser'
import VueWaypoint from 'vue-waypoint'
import VueRouter from 'vue-router'
import { Vue as VueIntegration } from '@sentry/integrations'
import App from './App.vue'
import router from './router'
import store from './store'
import constants from './constants'
import { paramsToFilterConfiguration } from '@/mixins/Filters'
import raf from 'raf'
import '../assets/tailwind.css'
import theme from '@/styles/tailwind.theme.js'
// vue-modal and vue-tailwind create a conflict
// at overriding Vue.prototype.$modal,
// so import only components we need
import TButton from 'vue-tailwind/dist/components/TButton.umd.js'

raf.polyfill()

if (process.env.NODE_ENV === 'production') {
  Sentry.init({
    dsn: 'https://91d6a27d4de14deba93bac991e05185f@sentry.io/1661534',
    integrations: [
      new VueIntegration({ Vue, attachProps: true, logErrors: true }),
    ],
  })
}

Vue.config.productionTip = false

Vue.prototype.$constants = constants
Vue.prototype.$api =
  process.env.NODE_ENV === 'production' ? '' : 'http://localhost:5000'

sync(store, router)

Vue.use(VueRouter)
Vue.use(VueSocialSharing)
Vue.use(VueClipboard)
Vue.use(Toasted)
Vue.use(TButton, theme.TButton)
Vue.use(VModal, { dialog: true })
Vue.use(VueWaypoint)
Vue.use(VueHotkey)

new Vue({
  router,
  store,
  render: h => h(App),
}).$mount('#app')

router.afterEach(to => {
  const config = paramsToFilterConfiguration(to.query)
  const keywords = Object.values(config)
    .flat()
    .filter(Boolean)
    .map(String)

  window.analytics.page('Filter', { keywords, searchterm: to.query.search })
})
