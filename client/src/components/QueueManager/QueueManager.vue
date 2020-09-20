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
      return window.urlForPublication.replace(':slug', publication.slug)
    },
  },
}
</script>

<template>
  <ul id="queue-manager" class="list-none">
    <li
      v-for="publication in publications"
      :key="publication.id"
      class="bg-superwhite flex justify-between w-full pt-8 pb-8 mb-8 pr-16"
    >
      <a class="w-2/4" :href="link(publication)">{{ publication.title }}</a>
      <div class="w-2/4">
        <button @click="$emit('move-up', publication.id)">
          <move-up-icon />
        </button>
        <button @click="$emit('move-down', publication.id)">
          <move-down-icon />
        </button>
        <button @click="$emit('remove', publication.id)">
          <remove-from-queue-icon />
        </button>
      </div>
    </li>
  </ul>
</template>

<style lang="less"></style>
