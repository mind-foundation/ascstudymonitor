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
    <ul class="list display-flex">
      <li v-for="d in disciplines" v-bind:key="d">
        <a
          class="font-bold mr-8 text-aqua"
          @click="toggleFilter('discipline', d)"
          >{{ d }}</a
        >
      </li>
    </ul>
  </div>
</template>

<style lang="less" scoped>
@import '~@/styles/variables';

.list {
  list-style: none;
  padding-bottom: 10px;
  user-select: none;

  a {
    &:hover {
      color: #607a9b;
    }
  }
}
</style>
