<script>
import Vue from 'vue'
import Paginate from 'vuejs-paginate'
import { mapGetters, mapState } from 'vuex'
import PublicationListItem from '@/components/PublicationListItem/PublicationListItem'

Vue.component('paginate', Paginate)

export default {
  name: 'single',
  mounted() {
    window.analytics.page('List')
  },
  components: {
    PublicationListItem,
  },
  computed: {
    ...mapState({
      loaded: state => state.loaded,
    }),
    ...mapGetters('publications', {
      publications: 'queryPublications',
    }),
    ...mapState('publications', {
      publication(state) {
        return state.items.find(
          p => p.slug === this.$store.state.route.params?.slug,
        )
      },
    }),
    ...mapState('recommendations', {
      recommendations: function() {
        return []
        // const a = state.items[this.publication.id]
        // return [a, a, a]

        // const recommendationIds = state.items[this.publication.id]
        // return recommendationIds?.map(id =>
        //   this.publications.find(p => p.id === id),
        // )
      },
    }),
  },
}
</script>

<template>
  <div id="container">
    <p v-if="!loaded">
      Loading..
    </p>
    <p v-else>
      No articles found matching your query. Try a different search instead.
      <router-link to="/">Or reset search.</router-link>
    </p>
    <ul>
      <publication-list-item
        v-for="publication in this.recommendations"
        :slug="publication.slug"
        :key="publication.id"
      />
      <router-link :to="{ path: '/publication/' + publication.slug }">{{
        publication.title
      }}</router-link>
    </ul>
  </div>

  <!-- <div v-if="publication.recommendations.length !== 0" class="pagination--wrapper">
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
  </div> -->
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
