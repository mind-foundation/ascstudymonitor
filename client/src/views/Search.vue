<script>
import SearchWidget from '@/components/SearchWidget'
export default {
  name: 'search',
  components: {
    SearchWidget,
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
    class="backgroud-blue text-white"
    :adaptive="true"
    width="100%"
    height="100%"
    @before-open="beforeOpen"
    :focus-trap="true"
    transition="fade"
  >
    <div
      class="modal-container reveal bg-blue flex flex-col justify-center items-center"
    >
      <div class="flex flex-row justify-around w-4/5 xl:w-3/5">
        <span class="inline-block mr-20 text-sm">fiter results</span>
        <ul class="flex flex-row flex-grow justify-between">
          <li>Dsciplines</li>
          <li>Journals</li>
          <li>Authors</li>
          <li>Years</li>
          <li>Keywords</li>
        </ul>
      </div>
      <div
        class="flex flex-grow flex-col justify-center items-center w-full h-40 "
      >
        <search-widget />
      </div>
      <div class="flex justify-center w-full sm:mb-10">
        <t-button
          classes="bg-blue pt-1 pb-1 pl-20 pr-20 text-white color-red"
          :variant="{
            error: true,
          }"
          tabindex="-1"
        >
          Show 8 results
        </t-button>
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
