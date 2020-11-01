<script>
export default {
  name: 'chevron-icon',
  props: ['expanded'],
}
</script>
<template>
  <svg
    class="menu__chev"
    xmlns="http://www.w3.org/2000/svg"
    width="35.912"
    height="20.077"
    viewBox="0 0 35.912 20.077"
    v-bind:class="{
      open: expanded,
    }"
  >
    <path
      class="a1"
      d="M36.107,2581,53,2597.9l-16.9,16.9"
      transform="translate(2615.851 -35.046) rotate(90)"
    />
  </svg>
</template>

<style scoped>
.menu__chev {
  margin-top: 9px;
  height: 10px;
  float: right;
  transform: rotate(90deg);
  transition: transform 0.2s ease-in;
}

.menu__chev.open {
  transform: rotate(0deg) !important;
}

.menu__chev .a1 {
  height: 10px;
  fill: none;
  stroke: white;
  stroke-width: 3px;
}
</style>
