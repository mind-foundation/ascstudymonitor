<template>
  <div class="container">
    <logo />
    <bubbles />
    <top-navigation />
    <!--       <hero-wrap>
        <router-view name="hero" />
      </hero-wrap>

      <router-view name="main" :filters="filters" />

 -->
    <keymap />
  </div>
  <about-modal />
  <search :filters="filters" />
</template>

<script>
// import List from './views/List.vue'
import TopNavigation from '/@/components/TopNavigation.vue'
import Search from '/@/views/Search.vue'
import Logo from '/@/components/Logo.vue'
import Bubbles from '/@/components/Bubbles.vue'
// import HeroWrap from '/@/components/HeroWrap.vue'
import Keymap from '/@/components/Keymap.vue'
import AboutModal from '/@/components/Modals/About.vue'
import $events from './events.js'

export default {
  name: 'App',
  components: {
    Bubbles,
    TopNavigation,
    AboutModal,
    Search,
    Logo,
    //     HeroWrap,
    Keymap,
  },
  provide: {
    $events,
  },
  data() {
    return {
      filters: getDefaultFilters(),
      showModal: false,
    }
  },
  watch: {
    filters: {
      deep: true,
      handler: function (_, newFilters) {
        // use replace instead of push until
        // navigating back could trigger a change in filters.
        // for that, we need two way router binding
        this.$router.replace({
          query: newFilters,
        })
        requestAnimationFrame(() => {
          window.scrollTo({
            top: 280,
            behavior: 'smooth',
          })
        })
      },
    },
  },
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
  },
}

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
</script>

<template></template>

<style>
html {
  -webkit-font-smoothing: antialised;
  -moz-osx-font-smoothing: grayscale;
}

body {
  background-color: #eef2f5;
  color: #00212b;
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

/* Disables double tap to zoom */
* {
  touch-action: manipulation;
}

.vm--modal {
  background: none !important;
}

/* global transition for modals */
.fade-enter,
.fade-leave-to {
  opacity: 0;
}
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease-in;
}
</style>
