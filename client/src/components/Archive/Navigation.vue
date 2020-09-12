<script>
import { mapGetters, mapState } from 'vuex'
import SlideUpDown from 'vue-slide-up-down'
import Filters from '@/mixins/Filters'
import IconFilters from '@/components/Icons/IconFilters'
import IconChevron from '@/components/Icons/IconChevron'

const accessors = {
  disciplines: 'disciplines',
  sources: 'sources',
  authors: 'authorNames',
  years: 'years',
  keywords: 'keywords',
}

export default {
  name: 'navigation',
  mixins: [Filters],
  components: {
    SlideUpDown,
    IconFilters,
    IconChevron,
  },
  data: () => ({
    open: [],
  }),
  methods: {
    keyToFacet(key) {
      return this.$constants.LABELS[key].toLowerCase().slice(0, -1)
    },
    handleMenuCategoryToggle(key) {
      // this.state = Array.from(new Set(...this.open, key))
      this.open = this.open.includes(key)
        ? this.open.filter(el => el !== key)
        : [...this.open, key]
    },

    toggleSortKey() {
      const newSortKey =
        this.$store.state.sortKey === 'count' ? 'label' : 'count'
      this.$store.commit('publications/setSortKey', newSortKey)
    },
  },
  computed: {
    ...mapState('publications', {
      publications: state => state.items,
      loaded: state => state.loaded,
    }),
    ...mapGetters('publications', {
      filterItems: 'summary',
      publicationsByKey: 'publicationsByKey',
    }),
    categories: function() {
      return Object.entries(accessors).reduce(
        (bag, [key, accessor]) => ({
          ...bag,
          [key]: {
            title: this.$constants.LABELS[key],
            total: Object.keys(this.publicationsByKey[accessor]).length,
            data: this.publications,
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
    <div>
      <div id="menu-header" @click="toggleSortKey()">
        <div
          id="mobile-only-search-icon"
          @click="$store.commit('toggleMobileSearch')"
        >
          Search
        </div>
        <icon-filters />
        <span>Filter</span>
      </div>
    </div>
    <span v-if="!loaded">Loading..</span>
    <div id="menu-tablet" v-else>
      <ul style="max-width: 250px" id="menu-content">
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
                v-for="s in filterItems[key].slice(0, 10)"
                :key="s.label"
                :data-value="s.label"
                @click="toggleFilter(keyToFacet(key), s.label)"
                :class="{
                  activeInFilter: isFilterActive(keyToFacet(key), s.label),
                }"
                aria-level="2"
              >
                {{ s.label }} ({{ s.count }})
              </li>
            </ul>
            <div
              v-if="filterItems[key].length > 10"
              class="show-more"
              @click="$modal.show('filter-modal')"
            >
              Show more
            </div>
          </slide-up-down>
        </li>
      </ul>

      <menu-bottom />
    </div>
  </nav>
</template>

<style lang="less" scoped>
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

  // @media @for-phone {
  //   width: 100%;
  //   height: 54px;
  //   // ios sticky fix
  //   z-index: 2;
  //   top: 0;
  //   left: 0;
  //   right: 0;

  //   overflow: hidden;
  //   -webkit-overflow-scrolling: touch;
  // }
}

#menu-tablet {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  justify-content: space-between;

  @media @for-phone {
    display: none;
  }
}
#menu-content {
  padding: 10px 10px 0 10px;
  overflow: auto;
  padding-bottom: 20px;
  list-style: none;
  margin-left: 0.5rem;
  margin-bottom: 1rem;
  line-height: 1.6;
  user-select: none;
  flex-grow: 1;
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

#menu-header {
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.2em;
  font-size: 1.2em;
  opacity: 0.5;
  display: inline-flex;
  user-select: none;
  width: 100%;
  text-align: left;
  padding-left: 1rem;
  box-sizing: border-box;

  @media @for-tablet-portrait-up {
    margin-top: 2em;
    align-items: center;
  }

  @media @for-phone {
    align-items: center;
    justify-content: space-between;
  }

  span {
    font-size: 1em;
    margin-left: 0.5em;
  }

  svg {
    height: 14px;
    margin-left: -1px;
  }
}

#mobile-only-search-icon {
  cursor: pointer;
  content: 'Search';

  @media @for-tablet-portrait-up {
    display: none;
  }
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

.show-more {
  background-color: white;
  color: #34557f;
  text-align: center;
  font-weight: bold;
  margin: 5px 0;
}
</style>
