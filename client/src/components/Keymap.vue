<script>
export default {
  name: 'keymap',
}
</script>

<template>
  <span v-hotkey="keymap">
    Press `enter` to toggle search! Hold `enter` to hide me!
  </span>
</template>

<script>
export default {
  methods: {
    handleKeyDown() {
      // if (this.searchWidgetFocused) {
      // } else {
      this.$modal.show('search-modal')
      // }
    },
  },
  computed: {
    // searchWidgetFocused
    //   return false, //this.$state.search.focused
    // },
    keymap() {
      return {
        enter: {
          keydown: this.handleKeyDown,
        },
      }
    },
  },
}
</script>

<style>
#logo {
  position: fixed;
  top: 10px;
  left: 14px;
}
</style>
