import { memoize } from 'lodash'
const log = require('debug')('filters')
import { FACETS } from '../constants'
log.enabled = process.env.NODE_ENV === 'development'

export const MULTIPLE_VALUE_SEPARATOR = '/'

export const slugifyMemo = memoize(slugify, (...args) => JSON.stringify(args))

export default {
  methods: {
    toggleFilter: function(facet, value) {
      const slugifiedValue = slugifyMemo(facet, value)
      const currentFilterConfiguration = this.$store.getters.filters
      const targetFilterConfiguration = toggleFacetInConfiguration(
        currentFilterConfiguration,
        facet,
        slugifiedValue,
      )
      const filterParams = filterConfigurationToParams(
        targetFilterConfiguration,
      )
      log('Set filters: %o', JSON.stringify(targetFilterConfiguration))

      const query = filterParams

      if (this.$store.state.route.query?.search) {
        query.search = this.$store.state.route.query.search
      }
      if (this.$store.state.route.query?.page) {
        query.page = this.$store.state.route.query.page
      }

      this.$router.push({ query })
    },

    isFilterActive(facet, value) {
      if (!value) {
        return false
      }

      const slugifiedValue = slugifyMemo(facet, value)
      const currentFilterConfiguration = this.$store.getters.filters
      const isActive = currentFilterConfiguration[facet]?.includes(
        slugifiedValue,
      )

      return isActive
    },
  },
}

export function paramsToFilterConfiguration(params) {
  return Object.entries(params).reduce((bag, [facet, valueString]) => {
    if (Object.values(FACETS).includes(facet)) {
      return {
        ...bag,
        [facet]: valueString
          .split(MULTIPLE_VALUE_SEPARATOR)
          .map(value => slugifyMemo(facet, value)),
      }
    } else {
      return bag
    }
  }, {})
}

export function filterConfigurationToParams(configuration) {
  return Object.entries(configuration).reduce(
    (bag, [facet, values]) => ({
      ...bag,
      [facet]: values.join(MULTIPLE_VALUE_SEPARATOR),
    }),
    {},
  )
}

export function toggleFacetInConfiguration(currentConfiguration, facet, value) {
  const newConfiguration = {
    ...currentConfiguration,
    [facet]: currentConfiguration[facet] || [],
  }

  const valueAtIndex = newConfiguration[facet].indexOf(value)
  if (valueAtIndex >= 0) {
    newConfiguration[facet] = newConfiguration[facet].filter(v => v !== value)
  } else {
    newConfiguration[facet].push(value)
  }

  if (newConfiguration[facet].length === 0) {
    delete newConfiguration[facet]
  }
  return newConfiguration
}

function slugify(facet, value) {
  if (!value) {
    return value
  }
  switch (facet) {
    case FACETS.YEAR:
      return parseInt(value, 10)
    case FACETS.JOURNAL:
    case FACETS.DISCIPLINE:
    case FACETS.AUTHOR:
      return value.toLowerCase().replace(/ /g, '-')
    default:
      return value
  }
}
