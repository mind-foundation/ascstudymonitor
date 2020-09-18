<script>
export default {
  name: 'by-line',
  props: {
    journal: String,
    year: Number,
  },
}
</script>
<template>
  <div class="container mt-2 flex text-sm" @click.stop>
    <a class="year text-gray" @click="toggleFilter('year', year)">{{ year }}</a>
    <a class="journal text-gray" @click="toggleFilter('journal', journal)">{{
      journal
    }}</a>
  </div>
</template>

<style lang="less" scoped>
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
