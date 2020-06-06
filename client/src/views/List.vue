<template>
  <div id="list">
    <div v-if="pagination.items.length == 0" class="message">
      <p v-if="!loaded">
        Loading..
      </p>
      <p v-else>
        No articles found matching your query. Try a different search instead.
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

    <div class="pagination--wrapper">
      <paginate
        :force-page="page"
        :page-count="pageCount"
        :page-range="3"
        :margin-pages="2"
        :click-handler="clickCallback"
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
        Showing {{ pagination.start }} to {{ pagination.end }} of
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
  methods: {
    clickCallback(page) {
      this.$router.replace({ query: { page } })
      setTimeout(() => {
        window.scrollTo({
          top: 0,
          behavior: 'smooth',
        })
      })
    },
  },
  computed: {
    loaded() {
      return this.$store.state.loaded
    },
    page() {
      const queryPage = this.$store.state.route.query.page
      return typeof queryPage === 'number' ? parseInt(queryPage) : 1
    },
    pageCount() {
      return Math.ceil(this.publications.length / this.$store.state.pageSize)
    },
    publications() {
      return this.$store.getters.queryPublications
    },
    pagination() {
      const { route, pageSize, publications } = this.$store.state
      const { page = 1 } = route.query
      const pageIndex = page - 1

      const items = this.publications.slice(pageIndex, pageIndex + pageSize)
      return {
        items,
        start: pageIndex + 1,
        end: pageIndex + items.length,
        total: publications.length,
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

.message {
  padding: 30px;
  color: #111;
  font-size: 1.1em;
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
