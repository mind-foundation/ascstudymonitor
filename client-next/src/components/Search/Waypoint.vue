<script>
import { EventBus } from '@/event-bus'

export default {
  name: 'search-waypoint',

  data: function() {
    return {
      intersectionOptions: {
        root: null,
        rootMargin: '0px 0px 0px 0px',
        threshold: [0, 1], // [0.25, 0.75] if you want a 25% offset!
      },
    }
  },

  methods: {
    onWaypoint({ going, direction }) {
      // console.info(going, direction, this.$waypointMap)
      if (
        going === this.$waypointMap.GOING_OUT &&
        direction === this.$waypointMap.DIRECTION_TOP
      ) {
        EventBus.$emit('searchbar.show')
      }

      if (
        going === this.$waypointMap.GOING_IN &&
        direction === this.$waypointMap.DIRECTION_BOTTOM
      ) {
        EventBus.$emit('searchbar.hide')
      }
    },
  },
}
</script>

<template>
  <div
    v-waypoint="{
      active: true,
      callback: onWaypoint,
      options: intersectionOptions,
    }"
  >
    <slot></slot>
  </div>
</template>
