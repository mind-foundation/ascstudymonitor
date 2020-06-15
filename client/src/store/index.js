import Vue from 'vue'
import Vuex from 'vuex'
import VuexPersistence from 'vuex-persist'
import localforage from 'localforage'
import { debounce } from 'lodash'
import publications from './modules/publications'
import recommendations from './modules/recommendations'

const log = require('debug')('store')
log.enabled = process.env.NODE_ENV === 'development'

const vuexLocal = new VuexPersistence({
  storage: localforage,
  asyncStorage: true,
  reducer: state => ({
    ...state,
    // Don’t persist route in between sessions to avoid
    // filter configuration conflicts between a manually
    // changed URL and the previous URL
    route: {},
    recommendations: {},
    mobileBarActivated: false,
  }),
  saveState: debounce((key, state, storage) => {
    requestAnimationFrame(() => {
      storage.setItem(key, state)
    })
  }),
})

Vue.use(Vuex)

const store = new Vuex.Store({
  modules: {
    publications,
    recommendations,
  },
  state: {
    mobileBarActivated: false,
    recommendations: {},
  },
  mutations: {
    toggleMobileSearch: state => {
      Vue.set(state, 'mobileBarActivated', !state.mobileBarActivated)
    },
  },
  getters: {},

  plugins: [vuexLocal.plugin],
})

export default store
