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

<style>
#bubble-left {
  position: absolute;
  top: 40px;
  left: -320px;
  width: 472px;
  height: 345px;

  z-index: -1;

  background: url('~assets/bubble_1.png') no-repeat;
}
#bubble-right {
  position: absolute;
  top: 40px;
  right: -400px;
  height: 564px;
  width: 751px;
  z-index: -1;

  background: url('~assets/bubble_2.png') no-repeat;
}
</style>
