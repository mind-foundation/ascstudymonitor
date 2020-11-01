<script>
// helpful for implementation:
// https://github.com/vuejs/vue-apollo/blob/v4/packages/test-e2e-composable-vue3/src/components/ChannelList.vue
import { watch, inject } from 'vue'
import InfiniteScrollingWaypoint from '/@/components/InfiniteScrollingWaypoint.vue'
import PublicationListItem from '/@/components/PublicationListItem/PublicationListItem.vue'
import SearchButton from '/@/components/Search/Button.vue'
import SearchBar from '/@/components/Search/Bar.vue'
import BackButton from '/@/components/BackButton.vue'
import SearchWaypoint from '/@/components/Search/Waypoint.vue'
import PublicationsQuery from '/@/graphql/queries/Publications.gql'
import { useQuery, useResult } from '@vue/apollo-composable'
import { FiltersSymbol } from '/@/symbols.ts'

export default {
  name: 'list',
  mounted() {
    // window.analytics.page('List')
  },
  components: {
    BackButton,
    InfiniteScrollingWaypoint,
    PublicationListItem,
    SearchBar,
    SearchButton,
    SearchWaypoint,
  },
  data: () => ({
    publications: {},
    cursor: null,
  }),
  // apollo: {
  // publications: {
  //   query: PublicationsQuery,
  //   variables() {
  //     const { search, ...fields } = this.$attrs.filters
  //     return {
  //       search: search,
  //       filters: fields,
  //     }
  //   },
  // },
  // },
  setup(props, context) {
    const $filters = inject(FiltersSymbol)
    const { search, ...fields } = $filters

    const { result, loading } = useQuery(PublicationsQuery, {
      search,
      filters: fields,
    })
    const publications = useResult(result, [])

    // watch(result, value => {
    //   console.log(value)
    // })

    return {
      loading,
      publications,
    }

    // apolloClient
    //   .query({
    //     query: PublicationsQuery, // gql`query DoHello($message: String!) { hello(message: $message) }`,
    //     variables: {
    //       search: search,
    //       filters: fields,
    //     },
    //   })
    //   .then(data => console.log(data))
    //   .catch(error => console.error(error))
  },
  created() {
    // this.$events.$on('infinityscroller.loadmore', () => {
    //   this.showMore()
    // })
    //console.log('hi')
  },
  computed: {
    hasActiveFilters() {
      const { search, ...fields } = this.$attrs.filters
      return search || Object.entries(fields).some(([, value]) => value.length)
    },
  },
  methods: {
    showMore() {
      this.$apollo.queries.publications.fetchMore({
        variables: {
          after: this.publications.edges[this.publications.edges.length - 1]
            .cursor,
        },
        updateQuery: (previousResult, { fetchMoreResult }) => {
          return {
            publications: {
              __typename: previousResult.publications.__typename,
              edges: [
                ...previousResult.publications.edges,
                ...fetchMoreResult.publications.edges,
              ],
              pageInfo: fetchMoreResult.publications.pageInfo,
            },
          }
        },
      })
    },
    resetSearch() {
      this.$events.$emit('filters.clear')
    },
  },
}
</script>

<template>
  <div
    id="list"
    :class="{
      mobileBarActivated: false,
    }"
  >
    <search-bar />

    <div class="mb-12 mt-2 flex items-center justify-center">
      <!-- Uncomment me when vue-waypoint works -->
      <!-- <search-waypoint>
        <search-button />
      </search-waypoint> -->
    </div>
    <!--
    <div
      v-if="publications.edges && publications.edges.length === 0"
      class="message"
    >
      <p class="text-center">
        No articles found matching your query. Try a different search instead.
        <a href="" @click="resetSearch"> Or reset search. </a>
      </p>
    </div> 
    <div class="relative" v-else>
      <back-button v-if="hasActiveFilters" label="Clear filters" />
    </div> -->
    <ul>
      <publication-list-item
        v-for="publication in publications.edges"
        :publication="publication.node"
        :slug="publication.node.slug"
        :key="publication.node.id"
      />
      <!-- <router-link :to="{ path: '/publication/' + publication.slug }">{{
        publication.title
      }}</router-link> -->
    </ul>
    <!-- <infinite-scrolling-waypoint
      v-if="publications.pageInfo && publications.pageInfo.hasNextPage"
    /> -->
  </div>
</template>

<style>
#list {
  margin-top: 30px;
  scroll-behavior: smooth;
  @media screen and (prefers-reduced-motion: reduce) {
    html {
      scroll-behavior: auto;
    }
  }

  transition: transform 0.1s ease-in-out;
}

.message {
  padding: 30px;
  color: #111;
  font-size: 1.1em;
  font-weight: 700;

  a {
    color: #34557f;
    margin-right: 8px;

    &:hover {
      color: #607a9b;
    }
  }
}

.pagination--wrapper {
  padding-right: 10px;
  a {
    cursor: pointer;
    display: block;
    height: 30px;
    width: 30px;
    padding: 0;
    line-height: 2.5em;
  }
  p {
    text-align: right;
    padding-right: 10px;
  }
}

.pagination--container {
  margin-top: 8px;
  display: flex;
  justify-content: flex-end;
}
.pagination--page-item {
  color: #333 !important;
  box-sizing: border-box;
  display: inline-block;
  min-width: 1.5em;
  margin-left: 2px;
  text-align: center;
  text-decoration: none !important;
  color: #333 !important;
  border: 0px solid #0000;
  border-radius: 0px;
}

.pagination--page-link:focus {
  outline: 0 !important;
}

.pagination--active {
  background: #dbdbdb;
  font-weight: bold;
}
</style>
