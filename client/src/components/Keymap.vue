<script>
export default {
  name: 'keymap',
}
</script>

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
