<template>
  <div id="app" class="lg:container lg:mx-aut4">
    <logo />
    <hero-wrap>
      <router-view name="hero" />
    </hero-wrap>
    <!-- <router-view name="main" /> -->
    <!-- <navigation />  -->

    <router-view name="main" />

    <keymap />

    <!-- <main id="main" v-if="enoughDataToContinue">
      <query-bar />
      <router-view />
    </main>

    <transition name="fade">
      <mindblower v-if="!enoughDataToContinue" />
    </transition>-->

    <filter-modal />
    <search-modal />
  </div>
</template>

<script>
import { mapState } from 'vuex'
import Navigation from '@/components/Navigation'
import QueryBar from '@/components/QueryBar'
import Mindblower from '@/components/Mindblower'
import InfoModal from '@/components/InfoModal'
import FilterModal from '@/components/FilterModal'
import SearchModal from '@/components/SearchModal'
import Logo from '@/components/Logo'
import HeroWrap from '@/components/HeroWrap'
import Keymap from '@/components/Keymap'

export default {
  components: {
    Navigation,
    QueryBar,
    Mindblower,
    InfoModal,
    FilterModal,
    SearchModal,
    Logo,
    HeroWrap,
    Keymap,
  },
  created() {
    this.$store.dispatch('publications/init')
    this.$store.dispatch('publications/load')
  },
  computed: mapState('publications', {
    enoughDataToContinue: state => state.items?.length > 0,
  }),
}
</script>

<style lang="less">
// @import '~@/styles/variables';
// @import '~@/styles/core';

html {
  // font-smooth: auto;
  -webkit-font-smoothing: antialised;
  -moz-osx-font-smoothing: grayscale;
}

body {
  background-color: #eef2f5;
  color: #0b2d3d;
  display: flex;
  flex-flow: column;
  align-items: center;
}

// .fade-enter-active,
// .fade-leave-active {
//   transition: opacity 0.5s;
// }
// .fade-enter, .fade-leave-to /* .fade-leave-active below version 2.1.8 */ {
//   opacity: 0;
// }
</style>
