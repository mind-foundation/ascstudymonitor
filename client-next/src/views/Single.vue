<script>
import PublicationDetail from '/@/components/PublicationDetail/PublicationDetail'
import RelatedBanner from '/@/components/PublicationDetail/RelatedBanner'
import PublicationListItem from '/@/components/PublicationListItem/PublicationListItem'
import PublicationQuery from '/@/graphql/queries/Publication.gql'
export default {
  name: 'single',
  components: {
    PublicationDetail,
    PublicationListItem,
    RelatedBanner,
  },
  mounted() {
    window.analytics.page('Single')
  },
  data: () => ({
    publication: {},
  }),
  apollo: {
    publication: {
      query: PublicationQuery,
      variables() {
        return {
          slug: this.$route.params?.slug,
        }
      },
    },
  },
}
</script>

<template>
  <div class="container">
    <publication-detail :publication="publication" />
    <related-banner />
    <ul>
      <publication-list-item
        v-for="recommendation in publication.recommendations"
        :publication="recommendation.publication"
        :slug="recommendation.publication.slug"
        :key="recommendation.publication.id"
      />
    </ul>
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
</style>
