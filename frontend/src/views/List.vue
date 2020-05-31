<template>
  <div id="list">
    <ul>
      <li v-for="publication in this.publications" :key="publication.id">
        <publication :publicationId="publication.id" />
        <!-- <router-link :to="{ path: '/publication/' + publication.slug }">{{
          publication.title
        }}</router-link> -->
      </li>
    </ul>

    <paginate
      :force-page="page"
      :page-count="pageCount"
      :page-range="3"
      :margin-pages="2"
      :click-handler="clickCallback"
      :prev-text="'Prev'"
      :next-text="'Next'"
      :container-class="'pagination'"
      :page-class="'page-item'"
    >
    </paginate>
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
    },
  },
  computed: {
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
  },
}
</script>

<style scoped lang="less">
#list {
  margin-top: 70px;
}
</style>
