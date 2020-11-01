<template>
  <div class="container">
    <logo />
    <bubbles />
    <top-navigation />
    <hero-wrap>
      <router-view name="hero" />
    </hero-wrap>

    <router-view name="main" />

    <keymap />
    <about-modal />
    <search />
  </div>
</template>

<script>
// import List from './views/List.vue'
import { inject, watch } from 'vue'
import TopNavigation from '/@/components/TopNavigation.vue'
import Search from '/@/views/Search.vue'
import Logo from '/@/components/Logo.vue'
import Bubbles from '/@/components/Bubbles.vue'
import HeroWrap from '/@/components/HeroWrap.vue'
import Keymap from '/@/components/Keymap.vue'
import AboutModal from '/@/components/Modals/About.vue'
import { FiltersSymbol } from '/@/symbols.ts'

export default {
  name: 'App',
  components: {
    Bubbles,
    TopNavigation,
    AboutModal,
    Search,
    Logo,
    HeroWrap,
    Keymap,
  },

  setup(props, context) {
    const $filters = inject(FiltersSymbol)

    watch($filters, value => {
      this.$router.replace({
        query: value,
      })
      requestAnimationFrame(() => {
        window.scrollTo({
          top: 280,
          behavior: 'smooth',
        })
      })
    })
  },
}
</script>

<template></template>

<style>
html {
  -webkit-font-smoothing: antialised;
  -moz-osx-font-smoothing: grayscale;
}

body {
  background-color: #eef2f5;
  color: #00212b;
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

/* Disables double tap to zoom */
* {
  touch-action: manipulation;
}

.vm--modal {
  background: none !important;
}

/* global transition for modals */
.fade-enter,
.fade-leave-to {
  opacity: 0;
}
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease-in;
}
</style>
