<script>
export default {
  name: 'infinite-scrolling-waypoint',
  data: function () {
    return {
      intersectionOptions: {
        rootMargin: '1500px',
      },
    }
  },
  methods: {
    onWaypoint({ going, direction }) {
      // console.info(going, direction, this.$waypointMap)
      if (
        going === this.$waypointMap.GOING_IN &&
        direction === this.$waypointMap.DIRECTION_TOP
      ) {
        this.$events.$emit('infinityscroller.loadmore')
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
  ></div>
</template>
