<script>
import { EventBus } from '@/event-bus'
import FilterIcon from '@/components/Icons/Filter'

export default {
  name: 'pill',
  components: {
    FilterIcon,
  },
  props: {
    filter: {
      type: Object,
      required: true,
    },
  },
  methods: {
    removeFilter() {
      EventBus.$emit('filters.disable', this.filter)
    },
  },
}
</script>
<template>
  <div
    class="wrapper inline-flex align-center justify-start items-center cursor-pointer"
    @click="removeFilter()"
  >
    <span class="inline-block mr-1">
      <filter-icon :field="filter.field" />
    </span>
    <span class="font-bold leading-7">{{ filter.label }}</span>
    <svg
      xmlns="http://www.w3.org/2000/svg"
      width="15.035"
      height="15.034"
      viewBox="0 0 15.035 15.034"
      class="block ml-3"
    >
      <g id="Group_43" data-name="Group 43" transform="translate(0.707 0.707)">
        <path
          id="Path_49"
          data-name="Path 49"
          class="cls-1"
          d="M5277.949,5922.349l13.621,13.62"
          transform="translate(-5277.949 -5922.349)"
        />
        <path
          id="Path_50"
          data-name="Path 50"
          class="cls-1"
          d="M5291.57,5922.349l-13.621,13.62"
          transform="translate(-5277.949 -5922.349)"
        />
      </g>
    </svg>
  </div>
</template>

<style scoped>
.wrapper {
  svg {
    width: 12px;
  }
  &:hover {
    svg {
      .cls-1 {
        stroke: #70838e;
      }
    }
  }
}
.cls-1 {
  fill: none;
  stroke: #c4d5e0;
  stroke-width: 2px;
  transition: stroke 0.05s ease-in-out;
}
</style>
