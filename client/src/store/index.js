import Vue from 'vue'
import Vuex from 'vuex'
import VuexPersistence from 'vuex-persist'
import localforage from 'localforage'
import Fuse from 'fuse.js'
import { transformPublication } from './helpers'
import { uniq, sortBy } from 'lodash'

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
  // distance: 100,
  // useExtendedSearch: false,
  threshold: 0.6,
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

const publicationFilterFn = {
  allApply: (pub, filter) => filter.every(v => v in pub.disciplines),
}

function publicationIsVisible(publication, filters) {}

const store = new Vuex.Store({
  state: {
    loaded: false,
    publications: [],
    pageSize: 20,
    sortKey: 'count',
  },
  mutations: {
    MUTATE_SORT_KEY: (state, newSortKey) => {
      Vue.set(state, 'sortKey', newSortKey)
    },
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
        process.env.NODE_ENV === 'production' ? '' : 'http://localhost:5000'
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
    distinctPublicationsKeys: function({ publications }) {},
    publicationsByKey: function({ publications }) {
      const years = {}
      const disciplines = {}
      const authorNames = {}
      const sources = {}

      for (const p of publications) {
        for (const a of p.authorNames) {
          authorNames[a] = authorNames[a] || []
          authorNames[a].push(p)
        }
        for (const d of p.disciplines) {
          disciplines[d] = disciplines[d] || []
          disciplines[d].push(p)
        }
        years[p.year] = years[p.year] || []
        years[p.year].push(p)

        sources[p.source] = sources[p.source] || []
        sources[p.source].push(p)
      }

      return {
        years: Object.values(years),
        disciplines: Object.values(disciplines),
        authorNames: Object.values(authorNames),
        sources: Object.values(sources),
      }
    },
    distinct({ publications }) {
      return {
        years: uniq(publications.map(p => p.year || 'None')),
        disciplines: uniq(publications.map(p => p.disciplines).flat()),
        authorNames: uniq(publications.map(p => p.authorNames).flat()),
        sources: uniq(publications.map(p => p.source)),
      }
    },
    summary(state, getters) {
      const { publications, sortKey } = state
      const { distinct } = getters

      const sort = array => {
        let sorted = sortBy(array, sortKey)
        if (sortKey === 'count') {
          sorted.reverse()
        }
        return sorted
      }

      return {
        disciplines: sort(
          distinct.disciplines.map(discipline => ({
            label: discipline,
            count: publications.filter(
              d => d.disciplines && d.disciplines.includes(discipline),
            ).length,
          })),
        ),
        sources: sort(
          distinct.sources.map(source => ({
            label: source,
            count: publications.filter(d => d.source === source).length,
          })),
        ),
        authors: sort(
          distinct.authorNames.map(authorName => ({
            label: authorName,
            count: publications.filter(d => d.authorNames.includes(authorName))
              .length,
          })),
        ),
        years: sort(
          distinct.years.map(year => ({
            label: year.toString(),
            count: publications.filter(d => d.year === year).length,
          })),
        ),
      }
    },
    queryPublications: function(state, getters, rootState) {
      const { search, filter } = rootState.route.query
      let basePublications = state.publications

      if (filter) {
        basePublications = basePublications.filter(pub =>
          Object.entries(filter).every(([key, included]) =>
            included.every(v => pub[key].includes(v)),
          ),
        )
      }

      if (search) {
        const fuse = new Fuse(basePublications, fuseOptions, index)

        basePublications = fuse.search(search)
        basePublications = basePublications.map(result => result.item)
      }
      return basePublications
    },
  },

  plugins: [vuexLocal.plugin],
})

export default store
