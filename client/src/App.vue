<template>
  <div id="app">
    <navigation />

    <main id="main" v-if="enoughDataToContinue">
      <query-bar />
      <router-view />
    </main>

    <transition name="fade">
      <mindblower v-if="!enoughDataToContinue" />
    </transition>

    <info-modal />

    <filter-modal />
  </div>
</template>

<script>
import { mapState } from 'vuex'
import Navigation from '@/components/Navigation'
import QueryBar from '@/components/QueryBar'
import Mindblower from '@/components/Mindblower'
import InfoModal from '@/components/InfoModal'
import FilterModal from '@/components/FilterModal'

export default {
  components: {
    Navigation,
    QueryBar,
    Mindblower,
    InfoModal,
    FilterModal,
  },
  created() {
    this.$store.dispatch('publications/init')
    this.$store.dispatch('publications/load')
  },
  computed: mapState('publications', {
    enoughDataToContinue: state => state.items.length > 0,
  }),
}
</script>

<style lang="less">
@import '~@/styles/variables';
@import '~@/styles/core';

#main {
  position: relative;
  @media @for-tablet-portrait-up {
    margin-left: @tablet-navigation-width;
    margin-top: 70px;
    width: calc(100vw - @tablet-navigation-width);
  }
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s;
}
.fade-enter, .fade-leave-to /* .fade-leave-active below version 2.1.8 */ {
  opacity: 0;
}
</style>
