<script>
export default {
  name: 'by-line',
  props: {
    source: String,
    year: Number,
  },
}
</script>
<template>
  <div class="container mt-2 flex text-sm" @click.stop>
    <a class="year text-gray" @click="toggleFilter('year', year)">{{ year }}</a>
    <a class="source text-gray" @click="toggleFilter('journal', source)">{{
      source
    }}</a>
  </div>
</template>

<style lang="less" scoped>
.entry__year_source a {
  display: inline-block;
  color: #333 !important;
}

.year {
  width: 42px;
}

.source {
  flex-grow: 1;
}
</style>
