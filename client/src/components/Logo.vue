<script>
export default {
  name: 'list-hero',
}
</script>

<template>
  <router-link to="/">
    <div id="logo">
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
