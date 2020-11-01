<script>
export default {
  name: 'list-hero',
  methods: {
    clearFilters() {
      this.$events.$emit('filters.clear')
    },
  },
}
</script>

<template>
  <router-link to="/">
    <div @click="clearFilters" id="logo">
      <img src="/assets/logo.png" />
    </div>
  </router-link>
</template>

<style scoped>
#logo {
  position: absolute;
  top: 20px;
  left: 20px;

  img {
    width: 120px;
  }
}
</style>
