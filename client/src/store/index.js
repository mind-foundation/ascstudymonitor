import Vue from 'vue'
import Vuex from 'vuex'
import VuexPersistence from 'vuex-persist'
import localforage from 'localforage'
import Fuse from 'fuse.js'
import { transformPublication } from './helpers'

const vuexLocal = new VuexPersistence({
  storage: localforage,
})

Vue.use(Vuex)

const fuseOptions = {
  // isCaseSensitive: false,
  // includeScore: false,
  // shouldSort: true,
  // includeMatches: false,
  // findAllMatches: false,
  // minMatchCharLength: 1,
  // location: 0,
  // threshold: 0.6,
  // distance: 100,
  // useExtendedSearch: false,
  keys: [
    { name: 'abstract', weight: 0.5 },
    { name: 'authors', weight: 1.2 },
    { name: 'disciplines', weight: 1.8 },
    { name: 'source', weight: 1.5 },
    { name: 'title', weight: 2.0 },
    { name: 'year', weight: 1.0 },
  ],
}

let index = null

export default new Vuex.Store({
  state: {
    loaded: false,
    publications: [],
    pageSize: 4,
  },
  mutations: {
    HYDRATE_SINGLE_PUBLICATION: (state, publication) => {
      const transformed = transformPublication(publication)
      Vue.set(state, 'publications', [transformed])
    },
    HYDRATE_ALL_PUBLICATIONS: (state, publications) => {
      publications = publications.map(transformPublication)
      Vue.set(state, 'publications', publications)
      Vue.set(state, 'loaded', true)

      setTimeout(() => {
        index = Fuse.createIndex(
          fuseOptions.keys.map(({ name }) => name),
          publications,
        )
      })
    },
  },
  actions: {
    loadPublications: context => {
      const prefix =
        process.env.NODE_ENV === 'production' ? '' : 'http://localhost:5000/'
      fetch(prefix + '/documents.json')
        .then(res => res.json())
        .then(data => context.commit('HYDRATE_ALL_PUBLICATIONS', data))
    },
    localLocalPublication: context => {
      const initialPublicationStringified = window.initialPublication
      if (initialPublicationStringified) {
        try {
          const document = JSON.parse(initialPublicationStringified)
          context.commit('HYDRATE_SINGLE_PUBLICATION', document)
        } catch (e) {
          console.error('Error parsing initial publication')
          console.error(e)
        }
      }
    },
  },
  modules: {},
  getters: {
    getPublications: state => state.publications,
    queryPublications: function(state, getters, rootState) {
      const { search } = rootState.route.query
      let basePublications = state.publications

      let hasFused = false
      if (search) {
        const fuse = new Fuse(basePublications, fuseOptions, index)

        basePublications = fuse.search(search)
        hasFused = true
      }

      if (hasFused) {
        basePublications = basePublications.map(result => result.item)
      }
      return basePublications
    },
  },

  plugins: [vuexLocal.plugin],
})
