<script>
import MoveUpIcon from '@/components/Icons/MoveUp'
import MoveDownIcon from '@/components/Icons/MoveDown'
import RemoveFromQueueIcon from '@/components/Icons/RemoveFromQueue'

export default {
  name: 'queue-manager',
  props: ['publications'],
  components: {
    MoveUpIcon,
    MoveDownIcon,
    RemoveFromQueueIcon,
  },
  methods: {
    link(publication) {
      return '/p/' + publication.slug
    },
  },
}
</script>

<template>
  <transition-group name="list" tag="ul" id="queue-manager" class="list-none">
    <li
      v-for="(publication, idx) in publications"
      :key="publication.id"
      class="bg-superwhite flex justify-between w-full pt-4 pb-4 pl-4 mb-8 pr-4 text-lg"
    >
      <div class="flex-shrink">
        <a :href="link(publication)" target="blank">
          {{ publication.title }}
        </a>
      </div>
      <div class="button-wrapper">
        <button
          @click="idx !== 0 && $emit('move-up', publication.id)"
          class="m-2"
          :class="{ disabled: idx == 0 }"
          title="Move up in queue"
        >
          <move-up-icon />
        </button>
        <button
          @click="
            idx !== publications.length - 1 &&
              $emit('move-down', publication.id)
          "
          class="m-2"
          :class="{ disabled: idx === publications.length - 1 }"
          title="Move down in queue"
        >
          <move-down-icon />
        </button>
        <button
          @click="$emit('remove', publication.id)"
          class="m-2"
          title="Remove from queue"
        >
          <remove-from-queue-icon />
        </button>
      </div>
    </li>
  </transition-group>
</template>

<style scoped>
.disabled {
  opacity: 0.3;
  cursor: not-allowed;
}

.button-wrapper {
  min-width: 125px;
}

.list-enter-active, .list-leave-active {
  transition: all 0.3s;
}
.list-enter {
  opacity: 0;
  transform: translateY(30px) scale(0.97);
}
.list-enter-to {
  opacity: 1;
  transform: translateY(0px);
}
.list-leave-to {
  opacity: 0;
  transform: translateY(30px) scale(0.97);
}
</style>
