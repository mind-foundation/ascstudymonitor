<script>
import { inject, ref } from 'vue'
import { EventsSymbol } from '/@/symbols.ts'
import Modal from '/@/components/Modal.vue'

export default {
  name: 'about-modal',
  components: {
    Modal,
  },
  setup() {
    const $events = inject(EventsSymbol)
    const show = ref(false)
    $events.on('modals.about.show', () => {
      show.value = true
      // window.analytics.page('About')
    })
    $events.on('modals.about.hide', () => {
      show.value = false
    })

    return {
      show,
    }
  },

  methods: {
    beforeOpen() {
      window.analytics.page('Modal.About')
    },
  },
}
</script>

<template>
  <!-- <button id="show-modal" @click="show = true">Show Modal</button> -->
  <!-- use the modal component, pass in the prop -->
  <transition name="fade">
    <modal v-if="show" @close="show = false">
      <!-- <div class="container modal-container bg-superwhite p-6">
    </div> -->

      <template v-slot:body>
        <h3 class="text-navy text-3xl mb-3">Thank you for being here</h3>

        <p class="leading-6 mb-6">
          The ASC Study Monitor is a curated, freely accessible, and regularly
          updated database of scholarly publications concerning altered states
          of consciousness (ASCs). The publications included in the ASC Study
          Monitor mainly cover the field of the “mind &amp; brain sciences”
          including philosophy, psychology, psychiatry, neuroscience, and
          medicine as well as natural sciences. Moreover, the monitor covers
          relevant publications from cultural studies and the social sciences
          that discuss altered states of consciousness. With the ASC Study
          Monitor, MIND provides a multidisciplinary reference base to
          researchers, practitioners, students, and the interested public. This
          aims to enable high-quality, evidence-based public discussions of
          consciousness, its alterations, capabilities, and pathologies.
        </p>

        <div class="text-center">
          <p class="italic mb-2">
            Visit the MIND website for more information and ways to support this
            project.
          </p>
          <p>
            <a
              href="https://mind-foundation.org/research/a-s-c-monitor?utm_source=asc-studymonitor&utm_medium=about-popup"
              target="_blank"
            >
              <button
                class="pt-3 pb-3 pl-10 pr-10 leading-none bg-navy hover:bg-danger hover:pl-12 hover:pr-12 bg-transparent text-white text-xs font-bold uppercase"
              >
                Go to the MIND website
              </button>
            </a>
          </p>
          <p class="mt-2">Made with ♥️ in Berlin</p>
        </div>
      </template>
    </modal>
  </transition>
</template>

<style scoped>
/* ::v-deep allow to target .modal-container specific to about modal */
::v-deep(.modal-container) {
  max-width: 540px;
  margin: 0px auto;
  padding: 20px 30px;
  background-color: #fff;
  border-radius: 2px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.33);
  font-family: Helvetica, Arial, sans-serif;
}

button {
  transition: all 0.2s ease-in-out;
}
</style>
