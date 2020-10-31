<script>
import DisciplineIcon from '@/components/Icons/Discipline.vue'
import { EventBus } from '@/event-bus'

export default {
  name: 'disciplines-list',
  props: {
    disciplines: {
      type: Array,
      required: true,
    },
  },
  components: {
    DisciplineIcon,
  },
  methods: {
    applyFilter(discipline) {
      EventBus.$emit('filters.apply', {
        field: 'disciplines',
        value: discipline,
      })
    },
  },
}
</script>
<template>
  <div class="flex" v-if="disciplines.length">
    <discipline-icon />
    <ul
      class="list list-none display-flex select-none flex-1 flex-reverse -m-1"
    >
      <li
        :key="d.value"
        v-for="d in disciplines"
        @click="applyFilter(d)"
        class="inline-block p-1 font-bold  text-aqua hover:text-lightblue cursor-pointer"
      >
        {{ d.value }}
      </li>
    </ul>
  </div>
</template>

<style scoped></style>
