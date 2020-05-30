<script>
import SlideUpDown from 'vue-slide-up-down'
import IconFilters from './IconFilters'
import IconChevron from './IconChevron'

function getDistinct(data, key) {
  console.log(data, key)
  // get distinct values for key from data
  return Array.from(new Set(data.flatMap(d => d[key]))).filter(Boolean)
}

const accessors = Object.freeze({
  disciplines: 'disciplines',
  source: 'sources',
  years: 'year',
  sources: 'sources',
})

export default {
  name: 'navigation',
  components: {
    SlideUpDown,
    IconFilters,
    IconChevron,
  },
  data: () => ({
    open: [],
  }),
  methods: {
    handleMenuCategoryToggle(key) {
      console.log('open', arguments)

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
    filterItemClick() {
      // const $target = $(event.target)
      // const key = $target.closest('li[data-key]').data('key')
      // const value = $target.closest('li[data-value]').data('value')
      // App.toggleFilter(key, value)
    },
  },
  computed: {
    loaded() {
      return this.$store.state.loaded
    },

    distinct() {
      const { publications } = this.$store.state
      console.log(this.$store)
      if (!this.loaded) {
        return {}
      }
      console.log('computing distinxt. accessors', publications)
      const distinct = Object.entries(accessors).reduce(
        (bag, [key, accessor]) => ({
          ...bag,
          [key]: getDistinct(publications, accessor),
        }),
        {},
      )

      console.log('distinct', distinct)

      return distinct
    },

    summaries() {
      const { publications } = this.$store.state
      if (!this.loaded) {
        return {}
      }
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
        authors: [...this.distinct.sources]
          .map(source => ({
            label: source,
            count: publications.filter(d => d.source === source).length,
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

      if (!this.loaded) {
        return {}
      }

      return Object.keys(accessors).reduce(
        (bag, key) => ({
          ...bag,
          [key]: {
            title: key[0].toUpperCase() + key.slice(1),
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
    <span v-if="!loaded">Loading</span>
    <ul style="max-width: 250px" id="menu-content" v-if="loaded">
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
          <span class="menu__category-link-label">{{ category.title }}</span
          >&nbsp;
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
              v-on:click="filterItemClick(s)"
              :class="{
                activeInFilter: false, //filters[key] && filters[key].includes(d.label),
              }"
              aria-level="2"
            >
              <a href="#">{{ s.label }} ({{ s.count }})</a>
            </li>
          </ul>
        </slide-up-down>
      </li>
    </ul>

    <!-- <div id="menu-bottom">
      <div aria-haspopup="true" id="menu-info" data-open="modal-about">
        <a>Info</a>
        <div class="reveal" id="modal-about" data-reveal aria-modal="true">
          <h3>Thank you for being here</h3>
          <p>
            The ASC Study Monitor is a curated, freely accessible, and regularly
            updated database of scholarly publications concerning altered states
            of consciousness (ASCs). The publications included in the ASC Study
            Monitor mainly cover the field of the “mind & brain sciences”
            including philosophy, psychology, psychiatry, neuroscience, and
            medicine as well as natural sciences. Moreover, the monitor covers
            relevant publications from cultural studies and the social sciences
            that discuss altered states of consciousness. With the ASC Study
            Monitor, MIND provides a multidisciplinary reference base to
            researchers, practitioners, students, and the interested public.
            This aims to enable high-quality, evidence-based public discussions
            of consciousness, its alterations, capabilities, and pathologies.
          </p>
          <p>
            Visit the MIND website for more information and ways to support this
            project.
          </p>
          <p class="lead">
            <a
              href="https://mind-foundation.org/project/asc-study-monitor?utm_source=asc-studymonitor&utm_medium=info-popup&utm_campaign=asc-studymonitor-pre-conference"
              target="_blank"
            >
              Go to the MIND website
            </a>
          </p>
          <button
            class="close-button"
            data-close
            aria-label="Close reveal"
            type="button"
          ></button>
        </div>
      </div>
      <div id="menu-about">
        <p>
          <span class="menu-bottom__asc">ASC</span>
          <span class="menu-bottom__study-monitor">Study Monitor</span>
        </p>
        <span class="menu-bottom__love">
          Made with &hearts; in Berlin
        </span>
      </div>
    </div> -->
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
}

#menu-content a {
  color: #fff;
  opacity: 0.9;
}

#menu-content a:hover {
  opacity: 1;
}

#menu-bottom {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: stretch;
  text-align: center;
}

#menu-info {
  padding: 10px;
  cursor: pointer;
  opacity: 0.9;
}

#menu-info:focus {
  outline: none;
}

#menu-info:hover {
  opacity: 1;
}

#menu-info a {
  color: #fff;
  font-size: 11pt;
}

#menu-about {
  border-top: 1px solid rgba(255, 255, 255, 0.15);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  height: 70px;
}

#menu-bottom p {
  display: inline;
  margin: 0 0 2px 0;
  font-size: 1.2em;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
}

.menu-bottom__asc {
  font-weight: 700;
  letter-spacing: 0.15em;
}

.menu-bottom__study-monitor {
  letter-spacing: 0.04em;
  font-weight: 300;
}
.menu-bottom__love {
  display: block;
  font-size: 0.8em;
  font-weight: 700;
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
}

.menu__category-link:hover {
  color: #fff;
  opacity: 1;
}

.menu__category-link-label {
  font-weight: 700;
  display: inline;
}

.menu__category-link-count {
  font-weight: 300;
  letter-spacing: 0.075em;
  color: rgba(255, 255, 255, 0.6);
}

.menu__category-collapsed {
  display: none;
}

.filterItem a {
  line-height: 1.8;
  padding: 0 !important;
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
