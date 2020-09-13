<template>
  <div
    id="container"
    class="max-w-3xl w-full flex items-center flex-col h-full"
  >
    <div class="search-wraper flex-grow w-full">
      <h1 class="text-center text-6xl font-light mb-6">Search and Filter</h1>
      <div class="t-4 border-2 border-white w-full">
        <input
          ref="input"
          class="primary-search bg-transparent color-white w-full p-2 pl-6 pb-3 font-light text-3xl"
          placeholder="Search for.."
          :value="query"
          :focus="handleFocus(true)"
          :blur="handleFocus(false)"
          @input="handleChange"
        />
      </div>
      <div
        class="t-4 border-2 border-white w-full border-t-0"
        v-if="this.suggestions.length"
      >
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
    <div class="button-wrapper w-full sm:w-3/6 sm:mb-10">
      <t-button
        tabindex="-1"
        :variant="this.suggestions.length > 0 ? 'results' : 'results-inactive'"
      >
        {{ suggestions.length > 0 ? suggestions.length : 'No' }} results
      </t-button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'search-widget',
  data: () => ({
    query: '',
    mobileExposureActive: true,
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
  }),

  methods: {
    handleFocus: () => {},
    handleChange({ target: { value } }) {
      let samples = [
        { title: 'Jasmin Jones', kind: 'Author' },
        { title: 'Jam', kind: 'Keyword' },
        { title: 'Jas', kind: 'Full Text Search' },
      ].map(x => ({
        ...x,
        id: [x.title, x.kind].join('-'),
      }))

      for (let i = samples.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * i)
        const temp = samples[i]
        samples[i] = samples[j]
        samples[j] = temp
      }

      if (Math.random() < 0.4) {
        samples.pop()
      }
      if (Math.random() < 0.2) {
        samples = []
      }

      this.suggestions = samples
      this.query = value
    },
  },

  mounted() {
    // setTimeout(() => {
    // console.log("timer fired")
    if (screen.height > 1024) {
      this.$refs.input.focus()
    }
    // })
  },

  computed: {},
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

.search-wraper {
  max-height: 400px;
}

.button-wrapper {
  width: 300px;
}

// ::placeholder {

// }
</style>
