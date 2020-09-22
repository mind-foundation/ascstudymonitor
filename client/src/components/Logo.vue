<script>
import { EventBus } from '@/event-bus'

export default {
  name: 'list-hero',
  methods: {
    clearFilters() {
      EventBus.$emit('filters.clear')
    },
  },
}
</script>

<template>
  <router-link to="/">
    <div @click="clearFilters" id="logo">
      <img src="../../assets/logo.png" />
    </div>
  </router-link>
</template>

<style scoped lang="less">
#logo {
  position: absolute;
  top: 10px;
  left: 14px;

  img {
    width: 106px;
    height: 26px;
  }
}
</style>
