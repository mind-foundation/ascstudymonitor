<template>
  <div id="app">
    <div class="container">
      <logo />
      <top-navigation />
      <bubbles />
      <hero-wrap>
        <router-view name="hero" />
      </hero-wrap>

      <router-view name="main" />

      <keymap />
      <!-- <router-view name="main" /> -->
      <!-- <navigation />  -->

      <!-- <main id="main" v-if="enoughDataToContinue">
      <query-bar />
      <router-view />
    </main>

    <transition name="fade">
      <mindblower v-if="!enoughDataToContinue" />
    </transition>-->

      <search />
    </div>
    <about-modal />
    <donate-modal />
  </div>
</template>

<script>
// import Navigation from '@/components/Navigation'
// import QueryBar from '@/components/QueryBar'
// import Mindblower from '@/components/Mindblower'
// // import InfoModal from '@/components/InfoModal'
import TopNavigation from '@/components/TopNavigation'
import Search from '@/views/Search'
import Logo from '@/components/Logo'
import Bubbles from '@/components/Bubbles'
import HeroWrap from '@/components/HeroWrap'
import Keymap from '@/components/Keymap'
import DonateModal from '@/components/Modals/Donate'
import AboutModal from '@/components/Modals/About'

export default {
  components: {
    // Navigation,
    // QueryBar,
    Bubbles,
    TopNavigation,
    // Mindblower,
    AboutModal,
    Search,
    DonateModal,
    Logo,
    HeroWrap,
    Keymap,
  },
}
</script>

<style lang="less">
html {
  -webkit-font-smoothing: antialised;
  -moz-osx-font-smoothing: grayscale;
}

body {
  background-color: #eef2f5;
  color: #0b2d3d;
  display: flex;
  flex-flow: column;
  align-items: center;
  font-family: 'Open Sans', sans-serif !important;
  font-size: 12px;
}

button:focus {
  outline: none !important;
}
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

.vm--modal {
  background: none !important;
}
</style>
