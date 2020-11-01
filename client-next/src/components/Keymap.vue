<script lang="ts">
import { inject, onMounted, onUnmounted } from 'vue'
import type { EventBridge } from '/@/events.ts'
import { EventsSymbol } from '/@/symbols.ts'

const EVENT = {
  KEY_UP: 'keyup',
}

const KEYS = {
  '13': 'ENTER',
  '27': 'ESCAPE',
}

export default {
  name: 'keymap',

  setup() {
    const $events: EventBridge = inject(EventsSymbol)

    function handler(ke: KeyboardEvent) {
      // console.log(ke)
      if (ke.type === EVENT.KEY_UP && KEYS[ke.keyCode] === 'ENTER') {
        $events.emit('modals.search.show')
      }

      // TODO: What if the user focusses an input field in search?
      // we want to make sure that ESC blurs but doesnt exit modal
      if (ke.type === EVENT.KEY_UP && KEYS[ke.keyCode] === 'ESCAPE') {
        $events.emit('modals.search.hide')
        $events.emit('modals.about.hide')
      }
    }

    onMounted(() => {
      document.addEventListener('keydown', handler)
      document.addEventListener('keyup', handler)
    })
    onUnmounted(() => {
      document.removeEventListener('keydown', handler)
      document.removeEventListener('keyup', handler)
    })
  },
}
</script>

<template>
  <div />
</template>
