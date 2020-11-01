<script lang="ts">
const EVENT = {
  KEY_UP: 'keyup',
}

const KEYS = {
  '13': 'ENTER',
  '27': 'ESCAPE',
}

export default {
  name: 'keymap',
  inject: ['$events'],
  mounted() {
    document.addEventListener('keydown', this.handler)
    document.addEventListener('keyup', this.handler)
  },
  unmounted() {
    document.removeEventListener('keydown', this.handler)
    document.removeEventListener('keyup', this.handler)
  },
  methods: {
    handler(ke: KeyboardEvent) {
      // console.log(ke)
      if (ke.type === EVENT.KEY_UP && KEYS[ke.keyCode] === 'ENTER') {
        this.$events.emit('modals.search.show')
      }

      // TODO: What if the user focusses an input field in search?
      // we want to make sure that ESC blurs but doesnt exit modal
      if (ke.type === EVENT.KEY_UP && KEYS[ke.keyCode] === 'ESCAPE') {
        this.$events.emit('modals.search.hide')
      }
    },
  },
}
</script>

<template>
  <div />
</template>
