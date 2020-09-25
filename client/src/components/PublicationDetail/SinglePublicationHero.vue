<script>
export default {
  name: 'single-publication-hero',
  props: ['title', 'file-attached'],
}
</script>

<template>
  <div
    class="w-full md:w-9/12 h-30 text-4xl m-auto mt-24 mb-16 text-center font-light leading-tight"
  >
    <h1>{{ title }}</h1>
    <download-icon
      @click="download(publication)"
      v-if="fileAttached"
      big="true"
    />
  </div>
</template>

<style scoped lang="less"></style>
