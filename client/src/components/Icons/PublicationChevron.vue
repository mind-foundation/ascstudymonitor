<script>
export default {
  name: 'publication-chevron-icon',
  props: ['expanded'],
}
</script>
<template>
  <svg
    xmlns="http://www.w3.org/2000/svg"
    class="chevron"
    data-id="${id}"
    viewBox="0 0 36 21"
    v-bind:class="{
      expanded: expanded,
    }"
  >
    <path
      class="a"
      d="M36.107,2581,53,2597.9l-16.9,16.9"
      transform="translate(2615.851 -35.046) rotate(90)"
    />
  </svg>
</template>

<style scoped>
.chevron {
  transition: transform 0.15s ease-in;
  padding: 10px; /* increase hit box */
  transform: rotate(-90deg);
  width: 54px;
  margin-top: 3px;
  cursor: pointer;
  path {
    user-select: none;
  }

  &.expanded {
    transform: rotate(0);
  }
}

.a {
  fill: none;
  stroke: #333;
  stroke-width: 3px;
}
</style>
