<template>
  <div
    id="container"
    class="max-w-3xl w-full flex items-center flex-col h-full"
  >
    <div class="search-wraper flex-grow w-full">
      <h1 class="text-center text-6xl font-light mb-6">Search and Filter</h1>
      <div class="t-4 border-2 border-white w-full">
        <input
          ref="input"
          class="primary-search bg-transparent color-white w-full p-2 pl-6 pb-3 font-light text-3xl"
          placeholder="Search for.."
          :value="searchInput"
          :focus="handleFocus(true)"
          :blur="handleFocus(false)"
          @input="handleChange"
        />
      </div>
      <div
        class="pl-3 pr-4 mt-4  text-black justify-around "
        v-if="filterList.length"
      >
        <ul class="list-none flex">
          <li
            :key="f.label"
            v-for="f in this.filterList"
            class="inline-block bg-superwhite p-2 mr-4"
          >
            <span class="inline-block mr-1">
              <filter-icon :field="f.field" /> </span
            >{{ f.label
            }}<span
              @click="removeFilter(f)"
              class="inline-block ml-2 cursor-pointer"
              >X</span
            >
          </li>
        </ul>
      </div>
      <div
        class="t-4 border-2 border-white w-full border-t-0"
        v-if="suggestions.publications.length"
      >
        <ul @click="$modal.hide('search-modal')">
          <li v-for="p in this.suggestions.publications" :key="p.id">
            <router-link :to="getLinkTo(p)">
              <div class="suggestion-row flex justify-between" :tabindex="0">
                <p class="py-2 px-6 font-bold text-left">{{ p.title }}</p>
                <p class="py-2 px-6 font-bold text-right">Publication</p>
              </div>
            </router-link>
          </li>
        </ul>
      </div>
      <div
        class="t-4 border-2 border-white w-full border-t-0"
        v-if="this.suggestions.fields.length"
      >
        <ul>
          <li v-for="fs in this.suggestions.fields" :key="fs.label">
            <div
              class="suggestion-row suggestion-row__field-suggestion flex justify-between"
              :tabindex="0"
              @click="addFilter(fs)"
            >
              <p class="py-2 px-6 font-bold text-left">{{ fs.label }}</p>
              <p class="py-2 px-6 font-bold text-right">
                {{ fs.kind }} ({{ fs.count }})
              </p>
            </div>
          </li>
        </ul>
      </div>
    </div>
    <div class="button-wrapper w-full sm:w-3/6 sm:mb-10">
      <button
        class="leading-none w-full pt-6 pb-6 pl-20 pr-20 text-navy bg-white text-lg font-bold"
        :class="{
          'opacity-25': suggestions.publications.length === 0,
        }"
        tabindex="-1"
      >
        {{
          suggestions.publications.length > 0
            ? `${suggestions.publications.length} results`
            : 'No matching publications'
        }}
      </button>
    </div>
  </div>
</template>

<script>
import SearchQuery from '@/graphql/Search.gql'
import FilterIcon from '@/components/Icons/Filter'
import { EventBus } from '@/event-bus'

const valueToLabel = value =>
  value.value ||
  (value.firstName ? [value.firstName, value.lastName].join(' ') : value)

export default {
  name: 'search-widget',

  components: {
    FilterIcon,
  },
  props: {
    filters: Object,
  },

  data: () => ({
    message: null,
    typing: null,
    debounce: null,
    searchInput: null,
    term: '',
    suggestions: {
      fields: [],
      publications: [],
    },
  }),

  apollo: {
    fieldSuggestions: {
      // has to be named like a root from resukt
      query: SearchQuery,
      variables() {
        return {
          term: this.term,
          filters: this.filters,
        }
      },
      result({ data }) {
        if (data) {
          this.suggestions = {
            publications: data.publications.edges.map(({ node }) => ({
              ...node,
            })),
            fields: data.fieldSuggestions.map(s => ({
              field: s.field,
              kind: {
                authors: 'Author',
                keywords: 'Keyword',
                year: 'Year',
                journal: 'Journal',
                disciplines: 'Discipline',
              }[s.field],
              score: s.score,
              value: s.value,
              label: valueToLabel(s.value),
              count: s.value.publicationCount,
            })),
          }
        }
      },
    },
  },

  methods: {
    handleFocus: () => {},

    handleChange(event) {
      this.message = null
      this.searchInput = event.target.value
      clearTimeout(this.debounce)
      this.debounce = setTimeout(() => {
        this.term = event.target.value
      }, 50)
    },
    getLinkTo(r) {
      return {
        path: window.urlForPublication.replace(':slug', r.slug),
      }
    },
    addFilter(filter) {
      this.searchInput = ''
      this.term = ''
      EventBus.$emit('filters.add', filter)
    },
    removeFilter(filter) {
      EventBus.$emit('filters.remove', filter)
    },
  },

  computed: {
    filterList() {
      return Object.entries(this.filters).reduce(
        (arr, [field, values]) => [
          ...arr,
          ...values.map(v => ({
            field,
            value: v,
            label: valueToLabel(v),
          })),
        ],
        [],
      )
    },
  },

  // mounted() {
  //   setTimeout(() => {
  //   if (screen.height > 1024) {
  //     this.$refs.input.focus()
  //   }
  // },
}
</script>

<style lang="less">
.primary-search {
  background-color: transparent;
  outline-style: none !important;
  box-shadow: none !important;
  border-color: transparent !important;

  &::placeholder {
    color: #fff;
    opacity: 0.3;
    // color: red;
  }
}

.suggestion-row {
  &:focus,
  &:hover {
    outline: 0;
    color: #000;
    background-color: #fff;

    &.suggestion-row__field-suggestion {
      cursor: copy;
    }
  }
}

.search-wraper {
  max-height: 400px;
}

.button-wrapper {
  width: 300px;
}

// ::placeholder {

// }
</style>
