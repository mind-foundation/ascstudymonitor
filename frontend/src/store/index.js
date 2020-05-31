import Vue from 'vue'
import Vuex from 'vuex'
import VuexPersistence from 'vuex-persist'
import localforage from 'localforage'
import Fuse from 'fuse.js'

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

let index = Fuse.createIndex(
  fuseOptions.keys.map(({ name }) => name),
  [],
)

export default new Vuex.Store({
  state: {
    loaded: false,
    publications: [],
    pageSize: 20,
  },
  mutations: {
    MUTATE_PUBLICATIONS: (state, publications) => {
      publications = publications.map(pub => ({
        ...pub,
        authorNames: pub.authors.map(a => `${a.first_name} ${a.last_name}`),
      }))
      Vue.set(state, 'publications', publications)
      Vue.set(state, 'loaded', true)

      console.log('setting index', publications.length)
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
      fetch('http://localhost:5000/documents.json')
        .then(res => res.json())
        .then(function(data) {
          context.commit('MUTATE_PUBLICATIONS', data)
        })
    },
    loadPublication: () => {
      // fetch('http://localhost:5000/documents.json')
      //   .then(res => res.json())
      //   .then(function(data) {
      //     context.commit('MUTATE_PUBLICATIONS', data)
      //   })
    },
  },
  modules: {},
  getters: {
    getPublications: state => state.publications,
    queryPublications: function(state, getters, rootState) {
      // if (!rootState.router) {
      //   return []
      // }
      const { page = 1, search } = rootState.route.query
      let basePublications = state.publications

      let hasFused = false
      if (search) {
        index
        console.log('looking for ' + search + ' in ', basePublications.length)
        const fuse = new Fuse(basePublications, fuseOptions, index)

        console.log(fuse)
        basePublications = fuse.search(search)
        console.log('fuse results', basePublications)
        hasFused = true
      }

      const pageIndex = page - 1
      console.log(pageIndex, pageIndex + state.pageSize)
      basePublications = basePublications.slice(pageIndex, pageIndex + 20)
      if (hasFused) {
        basePublications = basePublications.map(result => result.item)
      }
      return basePublications
    },
  },

  plugins: [vuexLocal.plugin],
})
