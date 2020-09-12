<script>
import IconScience from '@/components/Icons/IconScience.vue'
export default {
  name: 'disciplines-list',
  props: ['disciplines'],
  components: {
    IconScience,
  },
}
</script>
<template>
  <div class="flex">
    <icon-science />
    <ul class="list list-none display-flex select-none">
      <li class="mr-8" v-for="d in disciplines" v-bind:key="d">
        <a
          class="font-bold  text-aqua"
          @click="toggleFilter('discipline', d)"
          >{{ d }}</a
        >
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
