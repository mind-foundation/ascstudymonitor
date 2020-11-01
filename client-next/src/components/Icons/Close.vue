<script>
import { inject, ref } from 'vue'
import { EventsSymbol } from '/@/symbols.ts'

export default {
  name: 'close-icon',

  setup() {
    const $events = inject(EventsSymbol)
    const show = ref(false)

    const hide = () => $events.emit('modals.search.hide')

    return {
      hide,
    }
  },
}
</script>

<template>
  <div @click="hide()" class="cursor-pointer p-4">
    <svg
      xmlns="http://www.w3.org/2000/svg"
      width="51.757"
      height="51.757"
      viewBox="0 0 51.757 51.757"
    >
      <g transform="translate(-332.222 -21.222)">
        <rect
          width="67.882"
          height="5.314"
          transform="translate(332.222 69.222) rotate(-45)"
          fill="#fff"
        />
        <rect
          width="67.882"
          height="5.314"
          transform="translate(380.222 72.979) rotate(-135)"
          fill="#fff"
        />
      </g>
    </svg>
  </div>
</template>
