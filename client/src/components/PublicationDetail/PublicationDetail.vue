<script>
import SinglePublicationHero from './SinglePublicationHero.vue'

import AuthorsList from '@/components/PublicationListItem/AuthorsList'
import DisciplinesList from '@/components/PublicationListItem/DisciplinesList'
import SocialBar from '@/components/PublicationListItem/SocialBar'
import ByLine from '@/components/PublicationListItem/ByLine'

export default {
  name: 'publication-detail',
  components: {
    SinglePublicationHero,
    AuthorsList,
    DisciplinesList,
    SocialBar,
    ByLine,
  },
  props: {
    publication: Object,
  },
}
</script>

<template>
  <div class="container">
    <single-publication-hero
      :title="publication.title"
      :file-attached="publication.fileAttached"
    />
    <div class="content bg-superwhite flex pt-8 pb-8 mb-8 pr-16" @click.stop>
      <authors-list :authors="publication.authors" />

      <div class="flex flex-row justify-between">
        <by-line
          :year="publication.year.value"
          :journal="publication.journal && publication.journal.value"
        />
        <disciplines-list :disciplines="publication.disciplines" />
      </div>

      <div class="entry__abstract flex-row">
        <div class="entry__abstract_inner">
          <abstract-icon />
          <div class="entry__abstract_text" v-if="publication.abstract">
            {{ publication.abstract }}
          </div>
          <div class="entry__abstract_text" v-else>
            Abstract missing.
          </div>
        </div>
      </div>

      <div class="flex-row">
        <div
          class="entry__downloads-item"
          v-for="website in publication.websites"
          v-bind:key="website"
        >
          <link-icon />
          <a target="_blank" rel="noopener noreferrer" :href="website"
            >Visit publisher website
          </a>
        </div>

        <div class="entry__downloads-item" v-if="publication.fileAttached">
          <download-icon big="false" />
          <a
            target="_blank"
            rel="noopener noreferrer"
            :href="$api + '/p/' + publication.slug + '/download'"
            >Download full text</a
          >
        </div>
      </div>

      <div class="flex-row">
        <social-bar :publication="publication" />
      </div>
    </div>
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
</style>
