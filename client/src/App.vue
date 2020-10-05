<template>
  <div id="app">
    <div class="container">
      <logo />
      <top-navigation />
      <bubbles />
      <hero-wrap>
        <router-view name="hero" />
      </hero-wrap>

      <router-view name="main" :filters="filters" />

      <keymap />
      <search :filters="filters" />
    </div>
    <about-modal />
  </div>
</template>

<script>
import TopNavigation from '@/components/TopNavigation'
import Search from '@/views/Search'
import Logo from '@/components/Logo'
import Bubbles from '@/components/Bubbles'
import HeroWrap from '@/components/HeroWrap'
import Keymap from '@/components/Keymap'
import AboutModal from '@/components/Modals/About'
import { EventBus } from '@/event-bus'

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
export default {
  components: {
    Bubbles,
    TopNavigation,
    AboutModal,
    Search,
    Logo,
    HeroWrap,
    Keymap,
  },
  data: () => ({
    filters: getDefaultFilters(),
  }),
  watch: {
    filters: {
      deep: true,
      handler: function(_, newFilters) {
        this.$router.push({
          query: newFilters,
        })
      },
    },
  },
  created() {
    // safely! replace expected query params
    for (const key in getDefaultFilters()) {
      if (this.$route.query[key]) {
        this.filters[key] =
          key === 'year' // to be refactored..
            ? parseInt(this.$route.query[key])
            : this.$route.query[key]
      }
    }

    EventBus.$on('filters.apply', filter => {
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
          alreadyFiltered = this.filters[field].includes(value.year)
          !alreadyFiltered &&
            this.filters[field].push(prepareForGraphQl(value.year))
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

    EventBus.$on('filters.disable', filter => {
      const { field, value } = filter

      console.log(value)
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
    EventBus.$on('filters.clear', () => {
      // Dont do this, we want to keep the filters reference
      // this.filters = getDefaultFilters()

      // Overwrite properties instead
      Object.assign(this.filters, getDefaultFilters())
    })
  },
}
</script>

<style lang="less">
html {
  -webkit-font-smoothing: antialised;
  -moz-osx-font-smoothing: grayscale;
}

body {
  background-color: #eef2f5; // "white"
  color: #00212b; // "black"
  display: flex;
  flex-flow: column;
  align-items: center;
  font-family: 'Open Sans', sans-serif !important;
  font-size: 12px;
}

button:focus {
  outline: none !important;
}
*,
::after,
::before {
  -webkit-box-sizing: inherit;
  box-sizing: inherit;
}

// Disables double tap to zoom
* {
  touch-action: manipulation;
}

.vm--modal {
  background: none !important;
}
</style>
