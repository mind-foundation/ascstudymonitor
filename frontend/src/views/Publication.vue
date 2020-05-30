<template>
  <div class="entry">
    <span v-if="!publication">Loading..</span>
    <div v-if="publication">
      <ul class="entry__disciplines">
        <icon-science />
        <li v-for="d in publication.disciplines" v-bind:key="d">
          <a @click="query('disciplines', e)">{{ d }}</a>
        </li>
      </ul>

      <router-link :to="{ path: '/publication/' + publication.id }">
        <h3>
          {{ publication.title }}

          <icon-download v-if="publication.file_attached" />
        </h3>
      </router-link>

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

      <div class="entry__downloads" style="display: none">
        <div
          class="entry__downloads-item"
          v-for="website in publication.websites"
          v-bind:key="website"
        >
          <icon-link />
          <a target="_blank" rel="noopener noreferrer" :href="website"
            >Visit publisher website</a
          >
        </div>

        <icon-download v-if="publication.file_attached" />

        <a
          target="_blank"
          rel="noopener noreferrer"
          :href="'/download/' + publication.id"
          >Download full text</a
        >
      </div>
      <router-link :to="{ path: '/' }">Back to all</router-link>
    </div>
  </div>
</template>

<script>
// @ is an alias to /src
import IconDownload from '@/components/IconDownload.vue'
import IconAuthor from '@/components/IconAuthor.vue'
import IconLink from '@/components/IconLink.vue'
import IconAbstract from '@/components/IconAbstract.vue'
import IconScience from '@/components/IconScience.vue'

export default {
  name: 'Publication',
  components: {
    // HelloWorld,
    IconDownload,
    IconLink,
    IconAuthor,
    IconAbstract,
    IconScience,
  },
  props: ['publicationId'],
  computed: {
    publication() {
      console.log('A')
      const p = this.$store.state.publications.find(
        p => p.id === this.publicationId,
      )
      console.log('rendering ,publication is ', p)
      return p
    },
  },
}
</script>

<style>
.entry {
  margin: 0;
  padding: 12px 24px 12px 0;
}

.entry__chevron-wrapper svg {
  transition: transform 0.2s ease-in;
}

.entry ul {
  margin: 0;
}
.entry li {
  display: inline-block;
  font-weight: 700;
}

.entry__icon {
  width: 35px;
  min-width: 35px;
  display: inline-block;
}

.entry__icon .l {
  fill: none;
  stroke: #333;
  stroke-width: 1px;
}

.entry__disciplines {
  list-style: none;
  padding-bottom: 10px;
}
.entry__disciplines a {
  color: #34557f;
  font-size: 1.2em;
  font-weight: 700;
  margin-right: 8px;
}

.entry__disciplines a:hover {
  color: #607a9b;
}

.entry__disciplines .entry__icon {
  width: 32px;
  min-width: 32px;
}

.entry__disciplines svg {
  height: 20px;
  position: relative;
  bottom: -5px;
  left: 0.05em;
}

.entry__disciplines svg .a4 {
  fill: none;
  stroke: #34557f;
  stroke-width: 1px;
}

.entry__authors {
  list-style: none;
  padding-bottom: 10px;
  line-height: 2;
  display: inline-flex;
}

.entry__authors svg {
  height: 18px;
  position: relative;
  bottom: -4px;
  left: 4px;
}

.entry__authors svg .a3 {
  fill: none;
  stroke: #333;
  stroke-width: 1px;
}

.entry__authors a {
  color: #333;
  font-weight: 700;
  font-size: 1em;
  margin-right: 8px;
}

.entry__authors a:hover {
  color: #607a9b;
}

.entry__abstract {
  display: none;
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

.entry__downloads-icon {
  height: 24px;
  width: 24px;
  border-radius: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 10px;
}

.entry__downloads-icon__blue {
  background-color: rgb(27, 157, 164);
}

.entry__downloads-icon svg {
  height: 14px;
  position: relative;
  right: -0.03em;
  top: -0.02em;
}

.entry__downloads-item.big {
  display: inline-block;
  height: 24px;
  width: 24px;
  border-radius: 24px;
  /*margin-right: 10px;*/
}

.entry__downloads-item.big svg {
  height: 14px;
  position: relative;
  right: -0.01em;
  top: -0.02em;
}
</style>
