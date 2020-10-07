import Vue from 'vue'
import VueApollo from 'vue-apollo'
import VueSocialSharing from 'vue-social-sharing'
import VModal from 'vue-js-modal'
import VBodyScrollLock from 'v-body-scroll-lock'
import VueClipboard from 'vue-clipboard2'
import Toasted from 'vue-toasted'
import VueHotkey from 'v-hotkey'
import * as Sentry from '@sentry/browser'
import VueWaypoint from 'vue-waypoint'
import VueRouter from 'vue-router'
import { Vue as VueIntegration } from '@sentry/integrations'
import App from './App.vue'
import router from './router'
// import { paramsToFilterConfiguration } from '@/mixins/Filters'
import raf from 'raf'
import '../assets/tailwind.css'

import { createProvider } from './vue-apollo'

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

Vue.use(VueApollo)
Vue.use(VueRouter)
Vue.use(VueSocialSharing)
Vue.use(VueClipboard)
Vue.use(Toasted)
Vue.use(VModal, { dialog: true })
Vue.use(VBodyScrollLock)
Vue.use(VueWaypoint)
Vue.use(VueHotkey)

new Vue({
  router,
  apolloProvider: createProvider(),
  render: h => h(App),
}).$mount('#app')

// router.afterEach(to => {
//   const config = paramsToFilterConfiguration(to.query)
//   const keywords = Object.values(config)
//     .flat()
//     .filter(Boolean)
//     .map(String)

//   window.analytics.page('Filter', { keywords, searchterm: to.query.search })
// })
