import { memoize } from 'lodash'
const log = require('debug')('filters')
import { FACETS } from '../constants'
log.enabled = process.env.NODE_ENV === 'development'

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
      const newPath = serializeFilterConfiguration(targetFilterConfiguration)
      log('Set filters: %o', JSON.stringify(targetFilterConfiguration))

      this.$router.push({
        query: this.$store.state.route.query,
        path: newPath,
      })
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

export function deserializeFilterConfiguration(pathname) {
  const fragments = pathname.split('/').filter(Boolean)

  const FACET_VALUE_SEPARATOR = ':'
  const MULTIPLE_VALUE_SEPARATOR = ','

  return fragments.reduce((bag, current) => {
    const [facet, valueString] = current.split(FACET_VALUE_SEPARATOR)
    return {
      ...bag,
      [facet]: valueString
        .split(MULTIPLE_VALUE_SEPARATOR)
        .map(value => slugifyMemo(facet, value)),
    }
  }, {})
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

export function serializeFilterConfiguration(configuration) {
  return (
    Object.entries(configuration).reduce(
      (path, [facet, values]) => path + `/${facet}:${values.join(',')}`,
      '',
    ) || '/'
  )
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
