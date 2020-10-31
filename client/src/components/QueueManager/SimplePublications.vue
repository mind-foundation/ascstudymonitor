<script>
import AppendToQueueIcon from '@/components/Icons/AppendToQueue'

export default {
  name: 'simple-publications',
  components: { AppendToQueueIcon },
  props: ['publications'],
  methods: {
    link(publication) {
      return '/p/' + publication.slug
    },
  },
}
</script>

<template>
  <div id="simple-publications">
    <ul class="list-none">
      <li
        v-for="publication in publications"
        :key="publication.id"
        class="bg-superwhite flex justify-between w-full pt-8 pb-8 mb-8 pr-16"
      >
        <a class="w-2/4" :href="link(publication)">{{ publication.title }}</a>
        <div class="w-2/4">
          <button @click="$emit('append', publication.id)">
            <append-to-queue-icon />
          </button>
        </div>
      </li>
    </ul>
  </div>
</template>

<style></style>
