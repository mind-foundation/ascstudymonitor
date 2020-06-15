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
    <!-- <div id="nav">
      <router-link to="/">Home</router-link> |
      <router-link to="/about">About</router-link>
    </div> -->
    <info-modal />
    <filter-modal />
  </div>
</template>

<script>
import Navigation from './components/Navigation'
import QueryBar from './components/QueryBar'
import Mindblower from './components/Mindblower'
import InfoModal from './components/InfoModal'
import FilterModal from './components/FilterModal'

export default {
  components: {
    Navigation,
    QueryBar,
    Mindblower,
    InfoModal,
    FilterModal,
  },
  created() {
    this.$store.dispatch('localLocalPublication')
    this.$store.dispatch('loadPublications')
  },
  computed: {
    enoughDataToContinue() {
      return this.$store.state.publications.length
    },
  },
}
</script>
<style lang="less">
@import "~@/styles/variables";

*,
::after,
::before {
  -webkit-box-sizing: inherit;
  box-sizing: inherit;
}

// Disables double tap to zoom
* {
    touch-action: manipulation;
}

body {
  margin: 0;
  padding: 0;
  background: #fefefe;
  font-weight: 400;
  line-height: 1.5;
  color: #0a0a0a;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;

  color: #777;
  display: flex;
  flex-direction: row;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;

  font-family: 'Open Sans', sans-serif !important;
  font-size: 12px;
}
blockquote,
dd,
div,
dl,
dt,
form,
h1,
h2,
h3,
h4,
h5,
h6,
li,
ol,
p,
pre,
td,
th,
ul {
  margin: 0;
  margin-top: 0px;
  margin-right: 0px;
  margin-bottom: 0px;
  margin-left: 0px;
  padding: 0;
}

a {
  line-height: inherit;
  text-decoration: none;
  cursor: pointer;
}
p {
  margin-bottom: 1rem;
  font-size: inherit;
  line-height: 1.6;
  text-rendering: optimizeLegibility;
}

ul {
  list-style-type: none;
}

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
