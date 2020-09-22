<script>
import SearchWidget from '@/components/Search/Widget'
import CloseIcon from '@/components/Icons/Close'
import FilterBar from '@/components/FilterBar'
export default {
  name: 'search',

  props: {
    filters: Object,
  },

  components: {
    SearchWidget,
    CloseIcon,
    FilterBar,
  },
  methods: {
    beforeOpen() {
      setTimeout(() => {
        window.analytics.page('Search')
      }, 200)
    },
  },
}
</script>

<template>
  <modal
    name="search-modal"
    class=""
    :adaptive="true"
    width="100%"
    height="100%"
    @before-open="beforeOpen"
    :focus-trap="true"
    transition="fade"
  >
    <close-icon class="close-icon" />
    <div class="bg-blue h-full w-full flex flex-col justify-center">
      <div class="reveal container flex flex-col h-full  text-white">
        <filter-bar :filters="filters" />

        <div class="flex flex-grow flex-col items-center w-full h-40 mt-20 ">
          <search-widget :filters="filters" />
        </div>
      </div>
    </div>
  </modal>
</template>

<style lang="less">
.modal-backplate {
  position: fixed;
  top: 0;
  left: 0;
  bottom: 0;
  right: 0;
}

.close-icon {
  position: absolute;
  top: 30px;
  right: 20px;
}

.modal-container {
  height: 100%;
  width: 100%;

  border-radius: 2px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.33);
  transition: all 0.3s ease;

  h3 {
    margin-top: 0;
    color: #42b983;
    font-size: 1.9375rem;
  }
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s;
}
.fade-enter, .fade-leave-to /* .fade-leave-active below version 2.1.8 */ {
  opacity: 0;
}
// .prep-transition {
//   will-change: transform;
//   transform: translateY(0%);
//   transition: transform 1s;
// }

// .effect-leave-active {
//   transition: transform 1s;
// }

// .effect-enter {
//   transform: translateY(100%);
// }

// .effect-enter-to {
//   transform: translateY(0%);
// }
// .effect-leave {
//   transform: translateY(0%);
// }
// .effect-leave-to {
//   transform: translateY(100%);
// }

// .effect-background-enter-active {
//   transition: transform 0.5s;
// }
// .effect-background-leave-active {
//   transition: transform 0.5s;
// }

// .effect-background-enter {
//   transform: scale(1);
// }

// .effect-background-enter-to {
//   transform: scale(0.8);
// }
// .effect-background-leave {
//   transform: scale(0.8);
// }
// .effect-background-leave-to {
//   transform: scale(1);
// }
// https://github.com/codrops/FullscreenOverlayStyles/blob/master/css/style8.css
// tried above effect here but had perf issues.. maybe no problem
// on production. will need to check later
</style>
