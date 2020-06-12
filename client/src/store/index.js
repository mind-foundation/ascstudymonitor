import Vue from 'vue'
import Vuex from 'vuex'
import VuexPersistence from 'vuex-persist'
import localforage from 'localforage'
import Fuse from 'fuse.js'
import { transformPublication } from './helpers'
import { sortBy, isEmpty } from 'lodash'
import { paramsToFilterConfiguration, slugifyMemo } from '../mixins/Filters'
import { FACETS } from '../constants'

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
  }),
})

Vue.use(Vuex)

const fuseOptions = {
  // isCaseSensitive: false,
  // includeScore: false,
  // shouldSort: true,
  // includeMatches: false,
  findAllMatches: true,
  minMatchCharLength: 2,
  // location: 0,
  distance: 10000 / 0.6, // longest abstract currently 7637, gets scaled by threshold
  // useExtendedSearch: false,
  threshold: 0.6,
  keys: [
    // scores get scaled by text length,
    // so a high value makes sense for abstract
    { name: 'abstract', weight: 2.5 },
    { name: 'disciplines', weight: 1.8 },
    { name: 'authorNames', weight: 1.2 },
    { name: 'source', weight: 1.5 },
    { name: 'title', weight: 2.0 },
  ],
}

let index = null

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

      const needToUpdate =
        state.publications.length < 2 ||
        JSON.stringify(state.publications) !== JSON.stringify(publications)

      if (needToUpdate) {
        Vue.set(state, 'publications', publications)
      }
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
      const prefix = Vue.prototype.$api
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
    filters(state) {
      return paramsToFilterConfiguration(state.route.query || {})
    },
    publicationsByKey: function({ publications }) {
      const years = {}
      const disciplines = {}
      const authorNames = {}
      const sources = {}
      const keywords = {}

      for (const p of publications) {
        for (const a of p.authorNames) {
          authorNames[a] = authorNames[a] || []
          authorNames[a].push(p)
        }
        for (const d of p.disciplines) {
          disciplines[d] = disciplines[d] || []
          disciplines[d].push(p)
        }
        for (const d of p.keywords) {
          keywords[d] = keywords[d] || []
          keywords[d].push(p)
        }

        if (p.year) {
          years[p.year] = years[p.year] || []
          years[p.year].push(p)
        }

        if (p.source) {
          sources[p.source] = sources[p.source] || []
          sources[p.source].push(p)
        }
      }

      return {
        years,
        disciplines,
        authorNames,
        sources,
        keywords,
      }
    },
    distinct(state, getters) {
      const {
        years,
        disciplines,
        authorNames,
        sources,
        keywords,
      } = getters.publicationsByKey
      return {
        years: Object.keys(years).map(Number),
        disciplines: Object.keys(disciplines),
        authorNames: Object.keys(authorNames),
        sources: Object.keys(sources),
        keywords: Object.keys(keywords),
      }
    },
    summary(state, getters) {
      const { sortKey } = state
      const { distinct, publicationsByKey } = getters

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
            count: publicationsByKey.disciplines[discipline].length,
          })),
        ),
        sources: sort(
          distinct.sources.map(source => ({
            label: source,
            count: publicationsByKey.sources[source].length,
          })),
        ),
        authors: sort(
          distinct.authorNames.map(authorName => ({
            label: authorName,
            count: publicationsByKey.authorNames[authorName].length,
          })),
        ),
        years: sort(
          distinct.years.map(year => ({
            label: year,
            count: publicationsByKey.years[year].length,
          })),
        ),
        keywords: sort(
          distinct.keywords.map(year => ({
            label: year,
            count: publicationsByKey.keywords[year].length,
          })),
        ),
      }
    },
    queryPublications: function(state, getters, rootState) {
      const { search } = rootState.route.query
      let basePublications = state.publications
      const filters = getters.filters

      log('Got %o publications to chose from', basePublications.length)

      Object.entries(filters).forEach(([facet, visible]) => {
        const slugify = slugifyMemo.bind(null, facet)
        switch (facet) {
          case FACETS.YEAR:
            basePublications = basePublications.filter(p =>
              visible.includes(p.year),
            )
            break
          case FACETS.JOURNAL:
            basePublications = basePublications.filter(p =>
              visible.includes(slugify(p.source)),
            )
            break
          case FACETS.DISCIPLINE:
            basePublications = basePublications.filter(p =>
              p.disciplines.some(d => visible.includes(slugify(d))),
            )
            break
          case FACETS.AUTHOR:
            basePublications = basePublications.filter(p =>
              p.authorNames.some(a => visible.includes(slugify(a))),
            )
            break
          case FACETS.KEYWORD:
            basePublications = basePublications.filter(p =>
              p.keywords.some(k => visible.includes(slugify(k))),
            )
            break
          default:
            throw new Error('Filtering by unknown facet: ' + facet)
        }
      })

      log('Down to %o publications after filters', basePublications.length)

      if (search) {
        const useIndex = isEmpty(filters) ? index : null
        const fuse = new Fuse(basePublications, fuseOptions, useIndex)

        basePublications = fuse.search(search)
        basePublications = basePublications
          .map(result => result.item)
          .filter(Boolean) // item can be null if it was filtered above ()
        log(
          'Returning %o after searching for %o, used index: %s',
          basePublications.length,
          search,
          Boolean(useIndex),
        )
      }
      return basePublications
    },
  },

  plugins: [vuexLocal.plugin],
})

export default store
