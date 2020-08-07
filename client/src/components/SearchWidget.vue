<template>
  <div class="max-w-3xl w-full">
    <div class="t-4 border-2 border-white w-full">
      <input
        ref="input"
        class="primary-search bg-transparent color-white w-full p-4 font-light text-4xl"
        placeholder="Search for.."
        :value="query"
      />
    </div>
    <!-- <div class="bg-white">Results</div> -->
  </div>
</template>

<script>
export default {
  name: 'search-widget',
  data: () => ({
    query: '',
  }),

  mounted() {
    console.log('created')
    // setTimeout(() => {
    // console.log("timer fired")
    this.$refs.input.focus()
    // })
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

  // ::placeholder {

  // }
}
</style>
