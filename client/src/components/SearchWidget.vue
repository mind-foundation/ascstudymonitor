<template>
  <div id="container" class="max-w-3xl w-full">
    <div class="t-4 border-2 border-white w-full">
      <input
        ref="input"
        class="primary-search bg-transparent color-white w-full p-4 font-light text-4xl"
        placeholder="Search for.."
        :value="query"
        :focus="handleFocus(true)"
        :blur="handleFocus(false)"
      />
    </div>
    <div class="t-4 border-2 border-white w-full border-t-0">
      <ul>
        <li v-for="s in this.suggestions" :key="s.id">
          <div class="suggestion-row flex justify-between" :tabindex="0">
            <p class="py-2 px-6 font-bold text-left">{{ s.title }}</p>
            <p class="py-2 px-6 font-bold text-right">{{ s.kind }}</p>
          </div>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
export default {
  name: 'search-widget',
  data: () => ({
    query: '',
    mobileExposureActive: true,
  }),

  methods: {
    handleFocus: () => {},
  },

  mounted() {
    console.log('created')
    // setTimeout(() => {
    // console.log("timer fired")
    if (screen.height > 1024) {
      this.$refs.input.focus()
    }
    // })
  },

  computed: {
    suggestions() {
      return [
        { title: 'Jasmin Jones', kind: 'Author' },
        { title: 'Jam', kind: 'Keyword' },
        { title: 'Jas', kind: 'Full Text Search' },
      ].map(x => ({
        ...x,
        id: [x.title, x.kind].join('-'),
      }))
    },
  },
}
</script>

<style lang="less">
.primary-search {
  background-color: transparent;
  outline-style: none !important;
  box-shadow: none !important;
  border-color: transparent !important;

  &::placeholder {
    color: #fff;
    opacity: 0.3;
    // color: red;
  }
}

.suggestion-row {
  &:focus {
    outline: 0;
    color: #000;
    background-color: #fff;
  }
}

// ::placeholder {

// }
</style>
