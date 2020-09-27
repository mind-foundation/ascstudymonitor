<script>
import DisciplineIcon from '@/components/Icons/Discipline.vue'
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
}
</script>
<template>
  <div class="flex" v-if="disciplines.length">
    <discipline-icon />
    <ul class="list list-none display-flex select-none">
      <li class="mr-8" v-for="d in disciplines" :key="d.value">
        <a
          class="font-bold  text-aqua"
          @click="toggleFilter('discipline', d.value)"
        >
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
