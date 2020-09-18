<script>
import gql from 'graphql-tag'
import PublicationListItem from '@/components/PublicationListItem/PublicationListItem'
import SearchButton from '@/components/Search/Button'
import SearchBar from '@/components/Search/Bar'
import SearchWaypoint from '@/components/Search/Waypoint'

export default {
  name: 'list',
  mounted() {
    window.analytics.page('List')
  },
  components: {
    PublicationListItem,
    SearchButton,
    SearchBar,
    SearchWaypoint,
  },
  data: () => ({
    publications: {},
  }),
  apollo: {
    publications: {
      query: gql`
        {
          publications(first: 20) {
            edges {
              cursor
              node {
                id
                abstract
                authors {
                  firstName
                  lastName
                }
                created
                disciplines {
                  value
                }
                fileAttached
                id
                keywords {
                  value
                }
                slug
                journal {
                  value
                }
                title
                websites
                year {
                  value
                }
              }
            }

            pageInfo {
              hasNextPage
              endCursor
            }
          }
        }
      `,
    },
  },
}
</script>

<template>
  <div
    id="list"
    :class="{
      mobileBarActivated: false, //$store.state.mobileBarActivated,
    }"
  >
    <search-bar />
    <div class="mb-12 mt-2 flex items-center justify-center">
      <search-waypoint>
        <search-button />
      </search-waypoint>
    </div>
    <!-- <div v-if="pagination.items.length === 0" class="message">
      <p v-if="!loaded">
        Loading..
      </p>
      <p v-else>
        No articles found matching your query. Try a different search instead.
        <router-link to="/">Or reset search.</router-link>
      </p>
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
    <!--
    <div v-if="pagination.items.length !== 0" class="pagination--wrapper">
      <paginate
        v-model="page"
        :force-page="page"
        :page-count="pageCount"
        :page-range="3"
        :margin-pages="2"
        :prev-text="'&lt;'"
        :next-text="'&gt;'"
        :break-view-text="'…'"
        :container-class="'pagination--container'"
        :active-class="'pagination--active'"
        :page-class="'pagination--page-item'"
        :page-link-class="'pagination--page-link'"
        :prev-class="'pagination--page-item'"
        :next-class="'pagination--page-item'"
      >
      </paginate>
       -->
    <!-- <p>
        Showing {{ pagination.start + 1 }} to {{ pagination.end }} of
        {{ publications.length }} entries
      </p> -->
    <!-- </div> -->
  </div>
</template>

<style lang="less">
#list {
  margin-top: 30px;
  scroll-behavior: smooth;
  @media screen and (prefers-reduced-motion: reduce) {
    html {
      scroll-behavior: auto;
    }
  }

  transition: transform 0.1s ease-in-out;

  // @media @for-phone {
  //   margin-top: @mobile-header-height;

  //   &.mobileBarActivated {
  //     transform: translateY(34px);
  //   }
  // }
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
