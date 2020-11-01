<script>
export default {
  name: 'bubbles',
}
</script>

<template>
  <div>
    <div id="bubble-right" />
    <div id="bubble-left" />
  </div>
</template>

<style scoped>
#bubble-left {
  position: fixed;
  top: 40px;
  left: -280px;
  width: 472px;
  height: 345px;

  z-index: -1;

  background: url('/assets/bubble_1.png') no-repeat;
}
#bubble-right {
  position: fixed;
  top: 40px;
  right: 0;
  height: 564px;
  width: 400px;
  z-index: -1;

  background: url('/assets/bubble_2.png') no-repeat;
}
</style>
