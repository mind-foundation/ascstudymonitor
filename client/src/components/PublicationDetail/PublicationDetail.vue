<script>
import SinglePublicationHero from './SinglePublicationHero.vue'
import BackButton from '@/components/BackButton'
import AuthorsList from '@/components/PublicationListItem/AuthorsList'
import DisciplinesList from '@/components/PublicationListItem/DisciplinesList'
// import SocialBar from '@/components/PublicationListItem/SocialBar'
import Abstract from '@/components/PublicationListItem/Abstract'
import ByLine from '@/components/PublicationListItem/ByLine'
import KeywordsList from '@/components/PublicationListItem/KeywordsList'
import Links from '@/components/PublicationListItem/Links'

export default {
  name: 'publication-detail',
  components: {
    // SocialBar,
    Abstract,
    AuthorsList,
    BackButton,
    ByLine,
    DisciplinesList,
    KeywordsList,
    Links,
    SinglePublicationHero,
  },
  props: {
    publication: { type: Object, required: true },
  },
}
</script>

<template>
  <div class="container relative">
    <single-publication-hero
      :title="publication.title"
      :file-attached="publication.fileAttached"
    />
    <div
      class="content relative bg-superwhite flex flex-col pt-12 pb-12 mb-8 pl-12 pr-12 lg:pl-16 lg:pr-16"
      @click.stop
    >
      <back-button label="Publication index from the ASC Study Monitor" />
      <authors-list :authors="publication.authors" />
      <keywords-list :keywords="publication.keywords" />
      <abstract :abstract="publication.abstract" />

      <div class="flex flex-row justify-between mr-1 ml-1">
        <by-line
          :year="publication.year.value"
          :journal="publication.journal && publication.journal.value"
        />
        <disciplines-list :disciplines="publication.disciplines" />
      </div>

      <links :publication="publication" />

      <!-- <div class="flex-row">
        <social-bar :publication="publication" />
      </div> -->
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
