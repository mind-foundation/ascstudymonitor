<script>
export default {
  name: 'icon-publication-chevron',
  props: ['expanded'],
}
</script>
<template>
  <svg
    xmlns="http://www.w3.org/2000/svg"
    class="chevron"
    data-id="${id}"
    width="35.912"
    height="20.077"
    viewBox="0 0 35.912 20.077"
    v-bind:class="{
      expanded: expanded,
    }"
  >
    <defs></defs>
    <path
      class="a"
      d="M36.107,2581,53,2597.9l-16.9,16.9"
      transform="translate(2615.851 -35.046) rotate(90)"
    />
  </svg>
</template>

<style lang="less" scoped>
.chevron {
  transition: transform 0.2s ease-in;
  &.expanded {
    transform: rotate(-90deg);
  }
}

.a {
  fill: none;
  stroke: #333;
  stroke-width: 3px;
}
</style>
