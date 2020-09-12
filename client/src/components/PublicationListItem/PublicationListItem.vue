<script>
import SlideUpDown from 'vue-slide-up-down'
import { mapState } from 'vuex'
import SocialBar from '@/components/SocialBar.vue'

import IconDownload from '@/components/Icons/IconDownload.vue'

import IconLink from '@/components/Icons/IconLink.vue'
import IconAbstract from '@/components/Icons/IconAbstract.vue'
import IconPublicationChevron from '@/components/Icons/IconPublicationChevron.vue'
import Filters from '@/mixins/Filters'
import DisciplinesList from './DisciplinesList.vue'
import AuthorsList from './AuthorsList.vue'
import ByLine from './ByLine.vue'

export default {
  name: 'Publication',
  components: {
    ByLine,
    IconDownload,
    IconLink,
    AuthorsList,
    IconAbstract,
    DisciplinesList,
    IconPublicationChevron,
    SlideUpDown,
    SocialBar,
  },
  mixins: [Filters],
  data: () => ({
    expanded: null,
  }),
  props: ['slug', 'publicationId'],
  computed: {
    isDetailView() {
      return (
        this.publication &&
        this.$store.state.route.params?.slug === this.publication.slug
      )
    },
    ...mapState('publications', {
      publications: state => state.items,
      publication: function(state) {
        if (this.publicationId)
          return state.items.find(p => p.id === this.publicationId)
        else return state.items.find(p => p.slug === this.slug)
      },
    }),
    ...mapState('recommendations', {
      recommendations: function(state) {
        const recommendationIds = state.items[this.publication.id]
        return recommendationIds?.map(id =>
          this.publications.find(p => p.id === id),
        )
      },
    }),
  },
  methods: {
    toggleExpand() {
      if (this.isDetailView) return false
      this.expanded = !this.expanded
      if (this.expanded) {
        window.analytics.page('Publication')
        this.$store.dispatch('recommendations/get', this.publication.id)
      }
    },
    getLinkTo(r) {
      return {
        path: window.urlForPublication.replace(':slug', r.slug),
      }
    },
  },
  watch: {
    publication: function(publication) {
      this.$store.dispatch('recommendations/get', publication.id)
    },
  },
  created() {
    this.expanded = this.isDetailView
    if (this.expanded) {
      this.$store.dispatch('recommendations/get', this.publication.id)
    }
  },
}
</script>

<template>
  <li class="row pt-8 pb-8 mb-8 pr-16">
    <div class="chevron-wrapper" @click="toggleExpand">
      <icon-publication-chevron
        :expanded="expanded"
        :selectable="!isDetailView"
      />
    </div>

    <div class="content" @click.stop>
      <h3 class="text-2xl">
        {{ publication.title }}

        <icon-download
          @click="download(publication)"
          v-if="publication.file_attached"
          big="true"
        />
      </h3>

      <authors-list :authorNames="publication.authorNames" />

      <div class="flex flex-row justify-between">
        <by-line :year="publication.year" :source="publication.source" />

        <disciplines-list :disciplines="publication.disciplines" />
      </div>

      <slide-up-down :active="expanded" :duration="200">
        <div class="entry__abstract">
          <div class="entry__abstract_inner">
            <icon-abstract />
            <div class="entry__abstract_text" v-if="publication.abstract">
              {{ publication.abstract }}
            </div>
            <div class="entry__abstract_text" v-else>
              Abstract missing.
            </div>
          </div>
        </div>
      </slide-up-down>

      <div v-if="expanded">
        <div
          class="entry__downloads-item"
          v-for="website in publication.websites"
          v-bind:key="website"
        >
          <icon-link />
          <a target="_blank" rel="noopener noreferrer" :href="website"
            >Visit publisher website
          </a>
        </div>

        <div class="entry__downloads-item" v-if="publication.file_attached">
          <icon-download big="false" />
          <a
            target="_blank"
            rel="noopener noreferrer"
            :href="$api + '/documents/' + publication.id + '/download'"
            >Download full text</a
          >
        </div>

        <social-bar :publication="publication" />

        <div
          v-if="recommendations && recommendations.length"
          class="card-container"
        >
          <div v-for="r in recommendations" v-bind:key="r.id">
            <router-link :to="getLinkTo(r)">{{ r.title }}</router-link>
          </div>
        </div>
      </div>
      <!-- <router-link :to="{ path: '/' }">Back to all</router-link> -->
    </div>
  </li>
</template>

<style scoped lang="less">
.chevron-wrapper {
  min-width: 110px;
  display: flex;
  justify-content: center;
  align-items: flex-start;
  flex-grow: 1;
}

.row {
  display: flex;
  background-color: #fff;

  /* width: 100%; */

  h3 {
    margin-top: 0;
    color: #333;
    font-weight: 700;
    letter-spacing: 0.015em;
    margin-bottom: 10px;
  }

  ul {
    margin: 0;
  }

  li {
    display: inline-block;
    font-weight: 700;
  }
}

.entry__chevron-wrapper svg {
  transition: transform 0.2s ease-in;
}

.entry__icon {
  width: 35px;
  min-width: 35px;
  display: inline-block;

  .l {
    fill: none;
    stroke: #333;
    stroke-width: 1px;
  }
}

.entry__abstract {
  color: #333;
  line-height: 1.5;
  margin-bottom: 12px;
}

.entry__abstract_text {
  white-space: pre-line;
}

.entry__abstract_inner {
  display: inline-flex;
}

.entry__abstract svg {
  margin-left: 3px;
  margin-bottom: -1px;
}

.entry__downloads {
  display: inline-flex;
}

/*.entry__downloads-item .entry__icon svg{
  width: 30px;
  min-width: 30px;
}*/

.entry__downloads-item {
  margin-right: 24px;
  display: inline-flex;
  flex-direction: row;
  align-items: center;
  justify-content: stretch;
}

.entry__downloads-item a {
  color: #000;
  font-weight: 600;
}

.entry__downloads-item a:hover {
  color: #607a9b;
  text-decoration: none;
}

.entry__downloads-item a:hover {
  text-decoration: none;
  color: #607a9b;
}

.card-container {
  margin-top: 20px;
  display: flex;
  justify-content: space-evenly;
}
</style>
