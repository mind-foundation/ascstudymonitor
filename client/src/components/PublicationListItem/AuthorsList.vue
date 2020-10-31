<script>
import AuthorIcon from '@/components/Icons/Author.vue'
import { EventBus } from '@/event-bus'

export default {
  name: 'authors-list',
  props: {
    authors: Array,
  },
  components: {
    AuthorIcon,
  },
  methods: {
    format(author) {
      return author.firstName
        ? `${author.firstName} ${author.lastName}`
        : author.lastName
    },
    applyFilter(author) {
      EventBus.$emit('filters.apply', {
        field: 'authors',
        value: author,
      })
    },
  },
}
</script>
<template>
  <div class="container inline-flex mb-3">
    <div class="icon-holder">
      <author-icon />
    </div>
    <ul
      class="flex flex-wrap flex-1 list list-none select-none whitespace-no-wrap"
    >
      <li
        class="mr-2 cursor-pointer"
        v-for="(author, index) in authors"
        :key="index"
      >
        <a @click="applyFilter(author)">{{ format(author) }}</a>
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
