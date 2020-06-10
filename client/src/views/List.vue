<template>
  <div id="list">
    <div v-if="pagination.items.length === 0" class="message">
      <p v-if="!loaded">
        Loading..
      </p>
      <p v-else>
        No articles found matching your query. Try a different search instead.
        <router-link to="/">Or reset search.</router-link>
      </p>
    </div>
    <ul>
      <li v-for="publication in this.pagination.items" :key="publication.id">
        <publication :publicationId="publication.id" />
        <!-- <router-link :to="{ path: '/publication/' + publication.slug }">{{
          publication.title
        }}</router-link> -->
      </li>
    </ul>

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
      <p>
        Showing {{ pagination.start + 1 }} to {{ pagination.end }} of
        {{ publications.length }} entries
      </p>
    </div>
  </div>
</template>

<script>
import Vue from 'vue'
import Paginate from 'vuejs-paginate'
import Publication from './Publication'
Vue.component('paginate', Paginate)

export default {
  name: 'List',

  components: {
    Publication,
  },
  computed: {
    loaded() {
      return this.$store.state.loaded
    },
    page: {
      get() {
        const queryPage = this.$store.state.route.query?.page
        const page = parseInt(queryPage)
        if (page > 0 && page <= this.pageCount) {
          return page
        } else if (page > this.pageCount) {
          return this.pageCount
        } else {
          // catches page = NaN
          return 1
        }
      },
      set(page) {
        this.$router.push({
          query: {
            ...this.$store.state.route.query,
            page,
          },
        })
        setTimeout(() => {
          window.scrollTo({
            top: 0,
            behavior: 'smooth',
          })
        })
      },
    },
    pageCount() {
      return Math.ceil(this.publications.length / this.$store.state.pageSize)
    },
    publications() {
      return this.$store.getters.queryPublications
    },
    pageSize() {
      return this.$store.state.pageSize
    },
    pagination() {
      const { route, publications } = this.$store.state
      const { page = 1 } = route.query
      const pageIndex = Math.min(page, this.pageCount) - 1
      const total = this.publications.length
      const start = pageIndex * this.pageSize
      const end = Math.min((pageIndex + 1) * this.pageSize, total)
      const items = this.publications.slice(start, end)
      return {
        items,
        start,
        end,
        total,
      }
    },
  },
}
</script>

<style lang="less">
#list {
  margin-top: 70px;
  scroll-behavior: smooth;
  @media screen and (prefers-reduced-motion: reduce) {
    html {
      scroll-behavior: auto;
    }
  }
}

#list :nth-child(even) .entry {
  background-color: #f8f9fb;
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
