<template>
  <div class="entry">
    <span v-if="!publication">Loading..</span>
    <div class="row" v-if="publication">
      <div class="chevron-wrapper" @click="toggleExpand">
        <icon-publication-chevron
          :expanded="expanded"
          :selectable="!isDetailView"
        />
      </div>

      <div class="content" @click.stop>
        <ul class="entry__disciplines">
          <icon-science />
          <li v-for="d in publication.disciplines" v-bind:key="d">
            <a @click="toggleFilter('discipline', d)">{{ d }}</a>
          </li>
        </ul>

        <h3>
          {{ publication.title }}

          <icon-download
            @click="download(publication)"
            v-if="publication.file_attached"
            big="true"
          />
        </h3>

        <ul class="entry__authors">
          <icon-author />
          <div class="entry_authors_holder" @click.stop>
            <li
              v-for="(authorName, index) in publication.authorNames"
              :key="index"
            >
              <a @click="toggleFilter('author', authorName)">{{
                authorName
              }}</a>
            </li>
          </div>
        </ul>
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

        <div class="entry__year_source" @click.stop>
          <a
            class="entry__year_source__year"
            @click="toggleFilter('year', publication.year)"
            >{{ publication.year }}</a
          >
          <a @click="toggleFilter('journal', publication.source)">{{
            publication.source
          }}</a>
        </div>

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
    </div>
  </div>
</template>

<script>
// @ is an alias to /src
import SlideUpDown from 'vue-slide-up-down'
import { mapState } from 'vuex'
import SocialBar from '@/components/SocialBar.vue'
import IconDownload from '@/components/Icons/IconDownload.vue'
import IconAuthor from '@/components/Icons/IconAuthor.vue'
import IconLink from '@/components/Icons/IconLink.vue'
import IconAbstract from '@/components/Icons/IconAbstract.vue'
import IconScience from '@/components/Icons/IconScience.vue'
import IconPublicationChevron from '@/components/Icons/IconPublicationChevron.vue'
import Filters from '../mixins/Filters'

export default {
  name: 'Publication',
  components: {
    IconDownload,
    IconLink,
    IconAuthor,
    IconAbstract,
    IconScience,
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
      console.log('publication changed', publication.title)
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

<style scoped lang="less">
@import '~@/styles/variables';

.row {
  display: flex;
}

.chevron-wrapper {
  min-width: 110px;
  display: flex;
  justify-content: center;
  padding-top: 40px;

  @media @for-phone {
    min-width: 60px;
    align-items: start;
    padding-top: 64px;
  }
}

.entry {
  margin: 0;
  padding: 12px 20px 12px 0;
  /* width: 100%; */

  h3 {
    margin-top: 0;
    font-size: 1.8em;
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

.entry__disciplines {
  list-style: none;
  padding-bottom: 10px;
  user-select: none;

  a {
    color: #34557f;
    font-size: 1.2em;
    font-weight: 700;
    margin-right: 8px;

    &:hover {
      color: #607a9b;
    }
  }
}

.entry__authors {
  list-style: none;
  padding-bottom: 10px;
  line-height: 2;
  display: inline-flex;

  a {
    color: #333;
    font-weight: 700;
    font-size: 1em;
    margin-right: 8px;

    &:hover {
      color: #607a9b;
    }
  }

  svg {
    height: 18px;
    position: relative;
    bottom: -4px;
    left: 4px;

    .a3 {
      fill: none;
      stroke: #333;
      stroke-width: 1px;
    }
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

.entry__year_source {
  font-size: 0.9em;
  color: #212121bf;
  margin-bottom: 12px;
}

.entry__year_source a {
  display: inline-block;
  color: #333 !important;
}

.entry__year_source__year {
  width: 33px;
}

.entry__year_source a:hover {
  color: #607a9b;
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

.content {
  padding: 8px 24px 12px 0px;
}

.card-container {
  margin-top: 20px;
  display: flex;
  justify-content: space-evenly;
}
</style>
