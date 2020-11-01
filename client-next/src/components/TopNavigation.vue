<script>
import { inject, ref } from 'vue'
import { EventsSymbol } from '/@/symbols.ts'

export default {
  name: 'top-navigation',
  setup() {
    const $events = inject(EventsSymbol)
    return {
      handleClick: () => $events.emit('modals.about.show'),
    }
  },
}
</script>

<template>
  <div class="container flex flex-row-reverse mt-6">
    <a
      href="https://mind-foundation.org/donate/?utm_source=asc-studymonitor&utm_medium=donate-cta"
      target="_blank"
    >
      <button
        class="pt-3 pb-3 pl-10 pr-10 leading-none bg-navy hover:bg-danger bg-transparent text-white text-xs font-bold uppercase"
        tabindex="-1"
      >
        Donate
      </button>
    </a>

    <button
      class="pt-3 pb-3 pl-10 pr-10 leading-none border-transparent bg-transparent text-lightblue hover:text-navy text-xs font-bold uppercase"
      tabindex="-1"
      @click="handleClick()"
    >
      About
    </button>
  </div>
</template>

<style scoped>
.container button {
  letter-spacing: 2px;
}

button {
  transition: all 0.15s ease-in-out;
}
</style>
