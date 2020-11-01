<script>
import MoveUpIcon from '/@/components/Icons/MoveUp'
import MoveDownIcon from '/@/components/Icons/MoveDown'
import RemoveFromQueueIcon from '/@/components/Icons/RemoveFromQueue'

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
  <ul id="queue-manager" class="list-none">
    <li
      v-for="publication in publications"
      :key="publication.id"
      class="bg-superwhite flex justify-between w-full pt-4 pb-4 pl-4 mb-8 pr-16 text-lg"
    >
      <a class="flex-grow" :href="link(publication)" target="blank">{{
        publication.title
      }}</a>
      <div>
        <button @click="$emit('move-up', publication.id)" class="m-2">
          <move-up-icon />
        </button>
        <button @click="$emit('move-down', publication.id)" class="m-2">
          <move-down-icon />
        </button>
        <button @click="$emit('remove', publication.id)" class="m-2">
          <remove-from-queue-icon />
        </button>
      </div>
    </li>
  </ul>
</template>

<style></style>
