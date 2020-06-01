<template>
  <div class="entry">
    <span v-if="!publication">Loading..</span>
    <div class="row" v-if="publication" @click="toggleExpand">
      <div class="chevron-wrapper">
        <icon-publication-chevron :expanded="expanded" />
      </div>

      <div class="content">
        <ul class="entry__disciplines">
          <icon-science />
          <li v-for="d in publication.disciplines" v-bind:key="d">
            <a @click="query('disciplines', e)">{{ d }}</a>
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
          <div class="entry_authors_holder">
            <li
              v-for="authorName in publication.authorNames"
              v-bind:key="authorName"
            >
              <a @click="query('authors', authorName)">{{ authorName }}</a>
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

        <div class="entry__year_source">
          <a
            class="entry__year_source__year"
            @click="query('year', publixation.year)"
            >{{ publication.year }}</a
          >
          <a @click="query('source', publication.source)">{{
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
              :href="'/' + publication.id + '/download/'"
              >Download full text</a
            >
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
import IconDownload from '@/components/Icons/IconDownload.vue'
import IconAuthor from '@/components/Icons/IconAuthor.vue'
import IconLink from '@/components/Icons/IconLink.vue'
import IconAbstract from '@/components/Icons/IconAbstract.vue'
import IconScience from '@/components/Icons/IconScience.vue'
import IconPublicationChevron from '@/components/Icons/IconPublicationChevron.vue'

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
  },
  data: () => ({
    expanded: false,
  }),
  props: ['slug', 'publicationId'],
  computed: {
    isDetailView() {
      return (
        this.publication &&
        this.$store.state.route.params?.slug === this.publication.slug
      )
    },
    publication() {
      if (this.publicationId)
        return this.$store.state.publications.find(
          p => p.id === this.publicationId,
        )
      else return this.$store.state.publications.find(p => p.slug === this.slug)
    },
  },
  methods: {
    toggleExpand() {
      if (this.isDetailView) return false
      this.expanded = !this.expanded
    },
  },
  created() {
    if (this.isDetailView) {
      this.expanded = true
    }
  },
}
</script>

<style scoped lang="less">
.row {
  display: flex;
}

.chevron-wrapper {
  min-width: 110px;
  display: flex;
  justify-content: center;
  padding-top: 50px;
}

.entry {
  margin: 0;
  padding: 12px 24px 12px 0;
  width: 100%;

  h3 {
    margin-top: 0;
    font-size: 1.8em;
    color: #333;
    font-weight: 700;
    letter-spacing: 0.015em;
    margin-bottom: 10px;
    cursor: pointer;
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

.entry__abstract_inner {
  display: inline-flex;
}

.entry__abstract svg {
  margin-left: 3px;
  margin-bottom: -1px;
}

.entry__year_source {
  font-size: 0.9em;
  color: #333;
  opacity: 0.75;
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
</style>
