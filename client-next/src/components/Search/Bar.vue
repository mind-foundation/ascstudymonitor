<script lang="ts">
import { inject, ref, onMounted, onUnmounted } from 'vue'
import type { EventBridge } from '/@/events.ts'
import { EventsSymbol } from '/@/symbols.ts'
import SearchButton from '/@/components/Search/Button.vue'

export default {
  name: 'search-bar',
  components: {
    SearchButton,
  },
  data: function () {
    return {
      intersectionOptions: {
        root: null,
        rootMargin: '0px 0px 0px 0px',
        threshold: [0, 1], // [0.25, 0.75] if you want a 25% offset!
      },
    }
  },

  setup() {
    const $events: EventBridge = inject(EventsSymbol)
    const stuck = ref(false)

    onMounted(() => {
      $events.on('searchbar.show', () => {
        stuck.value = true
      })
      $events.on('searchbar.hide', () => {
        stuck.value = false
      })
    })
    onUnmounted(() => {
      $events.off('searchbar.show', () => {
        stuck.value = true
      })
      $events.off('searchbar.hide', () => {
        stuck.value = false
      })
    })

    return {
      stuck,
    }
  },
}
</script>

<template>
  <div class="sticky-wrap" :class="{ active: this.stuck }">
    <search-button />
  </div>
</template>

<style>
.search {
  position: relative;
  top: -2px;
}

.sticky-wrap {
  transition: transform 0.2s ease-in-out;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  transform: translateY(-60px);
  max-height: 60px; /* prevent wrapping on smallest screens */
}
.active {
  transform: translateY(30px);
}
</style>
