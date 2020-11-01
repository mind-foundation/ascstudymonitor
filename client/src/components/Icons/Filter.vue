<script>
import AuthorIcon from '@/components/Icons/Author.vue'
import DisciplineIcon from '@/components/Icons/Discipline.vue'
import JournalIcon from '@/components/Icons/Journal.vue'
import KeywordIcon from '@/components/Icons/Keyword.vue'

export default {
  name: 'filter-icon',
  props: {
    field: { type: String, required: true },
  },
  components: {
    AuthorIcon,
    DisciplineIcon,
    JournalIcon,
    KeywordIcon,
  },

  computed: {
    cmp() {
      return {
        authors: 'author-icon',
        disciplines: 'discipline-icon',
        journal: 'journal-icon',
        keywords: 'keyword-icon',
        year: 'span', // no icon for year?
      }[this.field]
    },
  },
}
</script>

<template>
  <component :is="cmp" />
</template>
