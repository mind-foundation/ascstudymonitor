<script>
import SlideUpDown from 'vue-slide-up-down'
import IconFilters from './IconFilters'
import IconChevron from './IconChevron'
import MenuBottom from './MenuBottom'

function getDistinct(data, key) {
  // get distinct values for key from data
  return Array.from(new Set(data.flatMap(d => d[key]))).filter(Boolean)
}

const accessors = Object.freeze({
  disciplines: 'disciplines',
  sources: 'source',
  authors: 'authors',
  years: 'year',
})

export default {
  name: 'navigation',
  components: {
    SlideUpDown,
    IconFilters,
    IconChevron,
    MenuBottom,
  },
  data: () => ({
    open: [],
    showModal: false,
  }),
  methods: {
    handleMenuCategoryToggle(key) {
      // this.state = Array.from(new Set(...this.open, key))
      this.open = this.open.includes(key)
        ? this.open.filter(el => el !== key)
        : [...this.open, key]

      // this.open =
      // const $target = $(event.target)
      // const $li = $target.closest('li')
      // const key = $li.data('key')
      // toggle(App.Menu.open, key)
      // const $ul = $li.find('ul')
      // $ul.stop().slideToggle(300)
    },
    navigate(key) {
      console.log(key)
      // const $target = $(event.target)
      // const key = $target.closest('li[data-key]').data('key')
      // const value = $target.closest('li[data-value]').data('value')
      // App.toggleFilter(key, value)
      this.$router.push({ path: '/', query: { search: key } })
    },
  },
  computed: {
    loaded() {
      return this.$store.state.loaded
    },

    distinct() {
      const { publications } = this.$store.state

      console.log(...Object.entries(accessors))
      return [
        ...Object.entries(accessors),
        ['authorNames', 'authorNames'],
      ].reduce(
        (bag, [key, accessor]) => ({
          ...bag,
          [key]: getDistinct(publications, accessor),
        }),
        {},
      )
    },

    summaries() {
      const { publications } = this.$store.state

      console.log(this.distinct)
      return {
        disciplines: [...this.distinct.disciplines]
          .map(discipline => ({
            label: discipline,
            count: publications.filter(
              d => d.disciplines && d.disciplines.includes(discipline),
            ).length,
          }))
          .sort((a, b) => b.count - a.count),
        sources: [...this.distinct.sources]
          .map(source => ({
            label: source,
            count: publications.filter(d => d.source === source).length,
          }))
          .sort((a, b) => b.count - a.count),
        authors: [...this.distinct.authorNames]
          .map(authorName => ({
            label: authorName,
            count: publications.filter(d => d.authorName === authorName).length,
          }))
          .sort((a, b) => b.count - a.count),
        years: [...this.distinct.years]
          .sort((a, b) => b - a)
          .map(year => ({
            label: year.toString(),
            count: publications.filter(d => d.year === year).length,
          })),
      }
    },
    categories() {
      const { publications } = this.$store.state

      const labels = {
        sources: 'Journals',
        authors: 'Authors',
        disciplines: 'Disciplines',
        years: 'Years',
      }

      return Object.keys(accessors).reduce(
        (bag, key) => ({
          ...bag,
          [key]: {
            title: labels[key],
            total: this.distinct[key].length,
            data: publications,
          },
        }),
        {},
      )
    },
  },
}
</script>

<template>
  <nav id="menu" role="navigation">
    <span v-if="!loaded">Loading..</span>
    <ul style="max-width: 250px" id="menu-content" v-else>
      <li class="menu__filter_header">
        <icon-filters />
        <span>Filter</span>
      </li>
      <li
        v-for="(category, key) in this.categories"
        :key="key"
        :data-key="key"
        aria-level="1"
      >
        <a
          href="#"
          class="menu__category-link"
          @click="handleMenuCategoryToggle(key)"
        >
          <span class="menu__category-link-label">{{ category.title }}</span>
          <span class="menu__category-link-count">{{ category.total }}</span>
          <icon-chevron :expanded="open.includes(key)" />
        </a>

        <slide-up-down :active="open.includes(key)" :duration="200">
          <ul class="menu vertical">
            <li
              class="filterItem"
              v-for="s in summaries[key]"
              :key="s.label"
              :data-value="s.label"
              @click="navigate(s.label)"
              :class="{
                activeInFilter: false, //filters[key] && filters[key].includes(d.label),
              }"
              aria-level="2"
            >
              {{ s.label }} ({{ s.count }})
            </li>
          </ul>
        </slide-up-down>
      </li>
    </ul>

    <menu-bottom />
  </nav>
</template>

<style lang="less" scoped>
#nav {
  padding: 30px;

  a {
    font-weight: bold;
    color: #2c3e50;

    &.router-link-exact-active {
      color: #42b983;
    }
  }
}

#menu {
  background-color: #34557f;
  position: fixed;
  height: 100vh;
  width: 240px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: stretch;
  color: #fff;
}

#menu-content {
  padding: 10px 10px 0 10px;
  overflow: scroll;
  padding-bottom: 20px;
  list-style: none;
  margin-left: 1.25rem;
  margin-bottom: 1rem;
  line-height: 1.6;
}

#menu-content > li {
  margin: 1em 0;
}

#menu-content ul {
  margin-top: 1em;
  margin-left: 1em;
}

#menu-content a {
  color: #fff;
  opacity: 0.9;
}

#menu-content a:hover {
  opacity: 1;
}

.menu__filter_header {
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.2em;
  font-size: 1.2em;
  opacity: 0.5;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.menu__filter_header span {
  font-size: 1em;
  margin-left: 0.5em;
}

.menu__filter_header svg {
  height: 14px;
  margin-left: -1px;
}

.menu__category-link {
  font-size: 1.4em;
  display: inline-block;
  padding-top: 10px !important;
  opacity: 0.9;
  width: 100%;

  line-height: inherit;
  text-decoration: none;
}

.menu__category-link:hover {
  color: #fff;
  opacity: 1;
}

.menu__category-link-label {
  font-weight: 700;
  display: inline-block;
  margin-right: 8px;
}

.menu__category-link-count {
  font-weight: 300;
  letter-spacing: 0.075em;
  color: rgba(255, 255, 255, 0.6);
}

.menu__category-collapsed {
  display: none;
}

.filterItem {
  line-height: 1.8;
  padding: 0 !important;
  cursor: pointer;
}

.filterItem.activeInFilter {
  font-weight: 700;
  position: relative;
}

.filterItem.activeInFilter::before {
  content: '';
  width: 8px;
  height: 8px;
  background-color: #f4b477;
  position: absolute;
  border-radius: 50%;
  left: -1.1em;
  top: 0.5em;
}
</style>
