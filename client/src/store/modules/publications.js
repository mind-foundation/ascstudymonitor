import Vue from 'vue'
import Fuse from 'fuse.js'
import { transformPublication } from '../helpers'
import { isEmpty, sortBy } from 'lodash'
import { FACETS } from '@/constants'
import { paramsToFilterConfiguration, slugifyMemo } from '@/mixins/Filters'
const log = require('debug')('store:publications')
log.enabled = true
const state = {
  items: [],
  pageSize: 20,
  sortKey: 'count',
  loaded: false,
}

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

const mutations = {
  setSortKey: (state, newSortKey) => {
    Vue.set(state, 'sortKey', newSortKey)
  },
  init: (state, publication) => {
    const transformed = transformPublication(publication)
    Vue.set(state, 'items', [transformed])
  },
  load: (state, publications) => {
    const items = state.items
    publications = publications.map(transformPublication)

    const needToUpdate =
      state.items.length < 2 ||
      JSON.stringify(items) !== JSON.stringify(publications)

    if (needToUpdate) {
      Vue.set(state, 'items', publications)
    }
    Vue.set(state, 'loaded', true)

    setTimeout(() => {
      global.__SEARCH_INDEX__ = Fuse.createIndex(
        fuseOptions.keys.map(({ name }) => name),
        publications,
      )
    })
  },
}

const actions = {
  load: context => {
    const prefix = Vue.prototype.$api
    fetch(prefix + '/documents.json')
      .then(res => res.json())
      .then(data => context.commit('load', data))
  },
  init: context => {
    const initialPublicationStringified = window.initialPublication
    if (initialPublicationStringified) {
      try {
        const document = JSON.parse(initialPublicationStringified)
        context.commit('init', document)
      } catch (e) {
        console.error('Error parsing initial publication')
        console.error(e)
      }
    }
  },
}

const getters = {
  filters(state, _, rootState) {
    return paramsToFilterConfiguration(rootState.route.query || {})
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
  queryPublications: function(
    { items },
    { filters },
    {
      route: {
        query: { search },
      },
    },
  ) {
    let basePublications = items

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
      const useIndex = isEmpty(filters) ? global.__SEARCH_INDEX__ : null
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
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
}
