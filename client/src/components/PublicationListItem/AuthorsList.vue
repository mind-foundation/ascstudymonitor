<script>
import IconAuthor from '@/components/Icons/IconAuthor.vue'
export default {
  name: 'authors-list',
  props: {
    authorNames: Array,
  },
  components: {
    IconAuthor,
  },
}
</script>
<template>
  <div class="container inline-flex">
    <div class="icon-holder">
      <icon-author />
    </div>
    <ul class="list list-none display flex select-none" @click.stop>
      <li class="mr-2" v-for="(authorName, index) in authorNames" :key="index">
        <a @click="toggleFilter('author', authorName)">{{ authorName }}</a>
      </li>
    </ul>
  </div>
</template>

<style lang="less" scoped>
.container {
  line-height: 2;

  a {
    color: #333;
    font-weight: 700;
    font-size: 1em;
    margin-right: 8px;

    &:hover {
      color: #607a9b;
    }
  }

  svg {
    height: 18px;
    position: relative;
    bottom: -2px;
    left: 4px;

    .a3 {
      fill: none;
      stroke: #333;
      stroke-width: 1px;
    }
  }
}

.icon-holder {
  width: 42px;
}
</style>
