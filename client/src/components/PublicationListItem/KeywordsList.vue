<script>
import KeywordIcon from '@/components/Icons/Keyword'
import { EventBus } from '@/event-bus'

export default {
  name: 'keywords-list',
  props: {
    keywords: {
      type: Array,
      required: true,
    },
  },
  components: {
    KeywordIcon,
  },
  methods: {
    applyFilter(keyword) {
      EventBus.$emit('filters.apply', {
        field: 'keywords',
        value: keyword,
      })
    },
  },
}
</script>
<template>
  <div class="container inline-flex mb-3" v-if="keywords.length">
    <div class="icon-holder">
      <keyword-icon />
    </div>
    <ul
      class="list list-none flex flex-wrap flex-1 select-none italic"
      @click.stop
    >
      <li
        :key="keyword.value"
        v-for="keyword in keywords"
        @click="applyFilter(keyword)"
        class="mr-4 whitespace-no-wrap text-lightgrey hover:text-lightblue cursor-pointer"
      >
        {{ keyword.value }}
      </li>
    </ul>
  </div>
</template>

<style scoped>
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
