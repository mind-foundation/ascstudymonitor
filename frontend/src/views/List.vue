<template>
  <div>
    <h2>List</h2>

    <ul>
      <li v-for="publication in this.publications" :key="publication.id">
        <router-link :to="{ path: '/publication/' + publication.id }">{{
          publication.title
        }}</router-link>
      </li>
    </ul>
  </div>
</template>

<script>
// @ is an alias to /src
// import HelloWorld from '@/components/HelloWorld.vue'

export default {
  name: 'List',
  components: {
    // HelloWorld,
  },
  computed: {
    publications() {
      const publications = this.$store.state.publications || []

      return publications.slice(0, 5)
    },
  },
}
</script>
