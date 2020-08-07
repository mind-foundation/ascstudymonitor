<script>
import SearchWidget from '@/components/SearchWidget'
export default {
  name: 'search-modal',
  components: {
    SearchWidget,
  },
  methods: {
    beforeOpen() {
      window.analytics.page('SearchModal')
    },
  },
}
</script>

<template>
  <modal
    name="search-modal"
    class="backgroud-blue text-white"
    :adaptive="true"
    width="100%"
    height="100%"
    @before-open="beforeOpen"
  >
    <div
      class="modal-container reveal bg-blue flex flex-col justify-center items-center"
    >
      <div class="flex flex-row justify-around w-4/5 xl:w-3/5">
        <span class="inline-block mr-20 text-sm">fiter results</span>
        <ul class="flex flex-row flex-grow justify-between">
          <li>Dsciplines</li>
          <li>Journals</li>
          <li>Authors</li>
          <li>Years</li>
          <li>Keywords</li>
        </ul>
      </div>
      <div
        class="flex flex-grow flex-col justify-center items-center w-full h-40 "
      >
        <search-widget />
      </div>
      <div class="flex justify-center w-full sm:mb-10">
        <t-button
          classes="bg-blue pt-1 pb-1 pl-20 pr-20 text-white color-red"
          :variant="{
            error: true,
          }"
        >
          Show 8 results
        </t-button>
      </div>
    </div>
  </modal>
</template>

<style lang="less">
.modal-backplate {
  position: fixed;
  top: 0;
  left: 0;
  bottom: 0;
  right: 0;
}
.modal-container {
  height: 100%;
  width: 100%;

  border-radius: 2px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.33);
  transition: all 0.3s ease;

  h3 {
    margin-top: 0;
    color: #42b983;
    font-size: 1.9375rem;
  }
}
</style>
