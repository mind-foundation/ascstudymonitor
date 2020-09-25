<template>
  <div id="app">
    <div class="container">
      <logo />
      <top-navigation />
      <bubbles />
      <hero-wrap>
        <router-view name="hero" />
      </hero-wrap>

      <router-view name="main" />

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
  created() {
    EventBus.$on('filters.add', filter => {
      const {
        field,
        value: { value },
      } = filter

      let alreadyFiltered

      switch (field) {
        case 'year':
        case 'journal':
        case 'disciplines':
        case 'keywords':
          alreadyFiltered = this.filters[field].includes(value)
          break
        case 'authors':
          alreadyFiltered = this.filters[field].some(
            ({ firstName, lastName }) =>
              firstName === value.firstName && lastName === value.lastName,
          )
          break
        default:
          throw new Error('Trying to filter for unknown field: ' + field)
      }
      const prepareForGraphQl = value => {
        if (value.value) return prepareForGraphQl(value.value)
        else {
          delete value.publicationCount
          delete value.__typename
          return value
        }
      }
      if (!alreadyFiltered) this.filters[field].push(prepareForGraphQl(value))
    })
    EventBus.$on('filters.remove', filter => {
      const { field, value } = filter

      switch (field) {
        case 'year':
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
      this.filters = getDefaultFilters()
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
