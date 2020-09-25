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
  top: 20px;
  left: 20px;

  img {
    width: 120px;
  }
}
</style>
