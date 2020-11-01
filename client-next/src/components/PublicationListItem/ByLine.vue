<script>
export default {
  name: 'by-line',
  props: {
    journal: Object,
    year: Object,
  },
  methods: {
    applyFilter(field, value) {
      this.$events.$emit('filters.apply', {
        field,
        value,
      })
    },
  },
}
</script>
<template>
  <div class="mb-5 flex text-sm" @click.stop>
    <a
      class="year text-gray hover:text-lightblue cursor-pointer"
      @click="applyFilter('year', year)"
      >{{ year.value }}</a
    >
    <a
      class="journal text-gray hover:text-lightblue cursor-pointer"
      @click="applyFilter('journal', journal)"
      v-if="journal"
      >{{ journal.value }}</a
    >
  </div>
</template>

<style scoped>
.entry__year_journal a {
  display: inline-block;
  color: #333 !important;
}

.year {
  width: 42px;
}

.journal {
  flex-grow: 1;
}
</style>
