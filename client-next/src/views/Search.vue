<script>
import { inject, ref } from 'vue'
import { EventsSymbol } from '/@/symbols.ts'
import SearchWidget from '/@/components/Search/Widget.vue'
import CloseIcon from '/@/components/Icons/Close.vue'
// // import FilterBar from '/@/components/FilterBar.vue'
import Modal from '/@/components/Modal.vue'

export default {
  name: 'search',

  // props: {
  //   filters: {
  //     type: Object,
  //     required: true,
  //   },
  // },

  components: {
    SearchWidget,
    CloseIcon,
    Modal,
    // FilterBar,
  },

  setup() {
    const $events = inject(EventsSymbol)
    const show = ref(false)
    $events.on('modals.search.show', () => {
      show.value = true
      // window.analytics.page('About')
    })
    $events.on('modals.search.hide', () => {
      show.value = false
    })

    return {
      show,
    }
  },
}
</script>

<template>
  <transition name="fade">
    <modal v-if="show" @close="show = false">
      <template v-slot:body>
        <close-icon class="close-icon" />
        <div class="bg-blue h-full w-full flex flex-col justify-center">
          <div class="reveal container flex flex-col h-full text-white">
            <!-- <filter-bar :filters="filters" /> -->

            <div class="flex flex-grow flex-col items-center w-full h-40 mt-20">
              <!-- <search-widget /> -->
            </div>
          </div>
        </div>
      </template>
    </modal>
  </transition>
</template>

<style scoped>
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

/* ::v-deep allow to target .modal-container specific to search modal */
::v-deep(.modal-container) {
  height: 100%;
  width: 100%;

  border-radius: 2px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.33);
  /* transition: all 0.3s ease; */

  h3 {
    margin-top: 0;
    color: #42b983;
    font-size: 1.9375rem;
  }
}

/* 
 .prep-transition {
   will-change: transform;
   transform: translateY(0%);
   transition: transform 1s;
 }

 .effect-leave-active {
   transition: transform 1s;
 }

 .effect-enter {
   transform: translateY(100%);
 }

 .effect-enter-to {
   transform: translateY(0%);
 }
 .effect-leave {
   transform: translateY(0%);
 }
 .effect-leave-to {
   transform: translateY(100%);
 }

 .effect-background-enter-active {
   transition: transform 0.5s;
 }
 .effect-background-leave-active {
   transition: transform 0.5s;
 }

 .effect-background-enter {
   transform: scale(1);
 }

 .effect-background-enter-to {
   transform: scale(0.8);
 }
 .effect-background-leave {
   transform: scale(0.8);
 }
 .effect-background-leave-to {
   transform: scale(1);
 }
 https://github.com/codrops/FullscreenOverlayStyles/blob/master/css/style8.css
 tried above effect here but had perf issues.. maybe no problem
 on production. will need to check later */
</style>
