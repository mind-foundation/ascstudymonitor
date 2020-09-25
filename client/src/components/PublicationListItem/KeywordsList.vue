<script>
import KeywordsIcon from '@/components/Icons/Keywords.vue'
export default {
  name: 'keywords-list',
  props: {
    keywords: {
      type: Array,
      required: true,
    },
  },
  components: {
    KeywordsIcon,
  },
  computed: {
    unwrapped() {
      return this.keywords.map(node => node.value)
    },
  },
}
</script>
<template>
  <div class="container inline-flex">
    <div class="icon-holder">
      <keywords-icon />
    </div>
    <ul
      class="list list-none flex flex-1 select-none text-lightgrey italic"
      @click.stop
    >
      <li class="mr-2" v-for="keyword in unwrapped" :key="keyword">
        {{ keyword }}
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
  flex-basis: 42px;
}
</style>
