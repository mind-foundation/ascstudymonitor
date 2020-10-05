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
    <ul class="list list-none display-flex select-none">
      <li class="mr-8" v-for="d in disciplines" :key="d.value">
        <a class="font-bold  text-aqua" @click="applyFilter(d)">
          {{ d.value }}
        </a>
      </li>
    </ul>
  </div>
</template>

<style lang="less" scoped>
.list {
  :last-child {
    margin-right: 0;
  }

  a {
    &:hover {
      color: #607a9b;
    }
  }
}
</style>
