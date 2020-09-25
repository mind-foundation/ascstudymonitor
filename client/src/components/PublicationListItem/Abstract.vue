<script>
import AbstractIcon from '@/components/Icons/Abstract.vue'

export default {
  name: 'abstract',
  props: {
    abstract: { type: String, required: true },
  },
  components: {
    AbstractIcon,
  },
}
</script>
<template>
  <div class="flex leading-8 mt-3 text-lightgrey text-base">
    <div class="icon-holder">
      <abstract-icon />
    </div>
    <div class="flex-1">
      {{ abstract }}
    </div>
  </div>
</template>

<style lang="less" scoped>
.icon-holder {
  flex-basis: 42px;
  position: relative;
  top: 1px;
}
</style>
