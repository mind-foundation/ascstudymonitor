import Vue from 'vue'
import VueSocialSharing from 'vue-social-sharing'
import { sync } from 'vuex-router-sync'
import VModal from 'vue-js-modal'
import VueClipboard from 'vue-clipboard2'
import Toasted from 'vue-toasted'
import * as Sentry from '@sentry/browser'
import { Vue as VueIntegration } from '@sentry/integrations'
import App from './App.vue'
import router from './router'
import store from './store'
import constants from './constants'

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

Vue.use(VueSocialSharing)
Vue.use(VueClipboard)
Vue.use(VModal)
Vue.use(Toasted)

new Vue({
  router,
  store,
  render: h => h(App),
}).$mount('#app')
