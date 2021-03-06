<script>
import AppendToQueueIcon from '@/components/Icons/AppendToQueue'

export default {
  name: 'simple-publications',
  components: { AppendToQueueIcon },
  props: ['publications', 'queue'],
  methods: {
    link(publication) {
      return '/p/' + publication.slug
    },
  },
}
</script>

<template>
  <div id="simple-publications">
    <transition-group name="list" tag="ul" class="list-none">
      <li
        v-for="publication in publications"
        :key="publication.id"
        class="bg-superwhite flex justify-between w-full p-4 pr-6 pb-8 mb-8"
      >
        <a :href="link(publication)">{{ publication.title }}</a>
        <div class="ml-4">
          <button
            @click="$emit('append', publication.id)"
            title="Append to queue"
          >
            <append-to-queue-icon />
          </button>
        </div>
      </li>
    </transition-group>
  </div>
</template>

<style>
.list-enter-active, .list-leave-active {
  transition: all 0.2s;
}
.list-leave-to {
  opacity: 0;
  transform: translateY(-30px);
}
</style>
