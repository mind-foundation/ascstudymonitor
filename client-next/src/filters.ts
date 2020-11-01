import { reactive } from 'vue'
function getDefaultFilters() {
  return {
    year: [],
    journal: [],
    authors: [],
    disciplines: [],
    keywords: [],
    search: undefined,
  }
}

const filters = reactive(getDefaultFilters())

export default filters

/*

_created() {
    // safely! replace expected query params
    for (const key in getDefaultFilters()) {
      if (this.$route.query[key]) {
        this.filters[key] =
          key === 'year' // to be refactored..
            ? parseInt(this.$route.query[key])
            : this.$route.query[key]
      }
    }

    this.$events.$on('filters.apply', filter => {
      const { field, value } = filter

      const prepareForGraphQl = value => {
        delete value.publicationCount
        delete value.__typename
        return value
      }

      var alreadyFiltered

      switch (field) {
        case 'search':
          this.filters[field] = value
          break
        case 'journal':
        case 'keywords':
        case 'disciplines':
          alreadyFiltered = this.filters[field].includes(value.value)
          !alreadyFiltered &&
            this.filters[field].push(prepareForGraphQl(value.value))
          break
        case 'year':
          alreadyFiltered = this.filters[field].includes(value.value)
          !alreadyFiltered &&
            this.filters[field].push(prepareForGraphQl(value.value))
          break
        case 'authors':
          alreadyFiltered = this.filters[field].some(
            ({ firstName, lastName }) =>
              firstName === value.firstName && lastName === value.lastName,
          )
          !alreadyFiltered && this.filters[field].push(prepareForGraphQl(value))
          break
        default:
          throw new Error('Trying to filter for unknown field: ' + field)
      }
    })

    this.$events.$on('filters.disable', filter => {
      const { field, value } = filter

      switch (field) {
        case 'year':
          this.filters[field] = this.filters[field].filter(
            activeFilter => activeFilter !== value,
          )
          break
        case 'journal':
        case 'disciplines':
        case 'keywords':
          this.filters[field] = this.filters[field].filter(
            activeFilter => activeFilter !== value,
          )
          break
        case 'authors':
          this.filters[field] = this.filters[field].filter(
            activeFilter =>
              !(
                activeFilter.firstName === value.firstName &&
                activeFilter.lastName === value.lastName
              ),
          )
          break
        default:
          throw new Error('Trying to filter for unknown field: ' + field)
      }
    })
    this.$events.$on('filters.clear', () => {
      // Dont do this, we want to keep the filters reference
      // this.filters = getDefaultFilters()

      // Overwrite properties instead
      Object.assign(this.filters, getDefaultFilters())
    })
    
*/
