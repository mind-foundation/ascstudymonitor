<script>
import QueueManager from '@/components/QueueManager/QueueManager'
import SimplePublications from '@/components/QueueManager/SimplePublications'
import Queue from '@/graphql/queries/Queue.gql'
import AppendToQueueMutation from '@/graphql/mutations/AppendToQueue.gql'
import MoveUpInQueueMutation from '@/graphql/mutations/MoveUpInQueue.gql'
import MoveDownInQueueMutation from '@/graphql/mutations/MoveDownInQueue.gql'
import RemoveFromQueueMutation from '@/graphql/mutations/RemoveFromQueue.gql'

const SEARCH_RESULTS_PAGE_SIZE = 10

export default {
  name: 'queue',
  components: {
    QueueManager,
    SimplePublications,
  },
  props: {
    channel: {
      type: String,
      required: true,
    },
  },
  data: () => ({
    queue: [],
    publications: [],
    searchInput: '',
    search: null,
  }),
  computed: {},
  methods: {
    handleQueueMutationUpdate(store, response, mutationName) {
      const updates = response.data[mutationName]

      const variables = {
        channel: this.channel,
        first: SEARCH_RESULTS_PAGE_SIZE,
        search: this.search,
      }

      const data = store.readQuery({
        query: Queue,
        variables,
      })
      data.queue = updates.queue

      store.writeQuery({ query: Queue, data, variables })
    },
    // Todo: Hanlde Mutations
    // https://apollo.vuejs.org/guide/apollo/mutations.html#server-side-example
    // https://github.com/Akryum/vue-apollo-todos/blob/master/src/components/TodoListItem.vue
    handleChange(event) {
      this.searchInput = event.target.value
      this.debounce = setTimeout(() => {
        this.search = event.target.value
      }, 200)
    },
    appendToQueue(publication) {
      this.$toasted.success('Successfully appended', {
        theme: 'toasted-primary',
        position: 'top-right',
        duration: 3000,
      })
      this.$apollo.mutate({
        mutation: AppendToQueueMutation,
        variables: {
          channel: this.channel,
          publication: publication,
        },
        update: (store, response) => {
          this.handleQueueMutationUpdate(store, response, 'appendToQueue')
        },
      })
    },
    moveUpInQueue(publication) {
      this.$toasted.success('Succesfully prioritized', {
        theme: 'toasted-primary',
        position: 'top-right',
        duration: 3000,
      })
      this.$apollo.mutate({
        mutation: MoveUpInQueueMutation,
        variables: {
          channel: this.channel,
          publication: publication,
        },
        update: (store, response) => {
          this.handleQueueMutationUpdate(store, response, 'moveUpInQueue')
        },
      })
      // setTimeout(() => {
      //   this.$apollo.queries.queue.refresh()
      // }, 300)
    },
    moveDownInQueue(publication) {
      this.$toasted.success('Succesfully deprioritized', {
        theme: 'toasted-primary',
        position: 'top-right',
        duration: 3000,
      })
      this.$apollo.mutate({
        mutation: MoveDownInQueueMutation,
        variables: {
          channel: this.channel,
          publication: publication,
        },
        update: (store, response) => {
          this.handleQueueMutationUpdate(store, response, 'moveDownInQueue')
        },
      })
    },
    removeFromQueue(publication) {
      this.$toasted.success('Succesfully removed', {
        theme: 'toasted-primary',
        position: 'top-right',
        duration: 3000,
      })
      this.$apollo.mutate({
        mutation: RemoveFromQueueMutation,
        variables: {
          channel: this.channel,
          publication: publication,
        },
        update: (store, response) => {
          this.handleQueueMutationUpdate(store, response, 'removeFromQueue')
        },
      })
    },
  },
  apollo: {
    queue: {
      query: Queue,
      variables() {
        return {
          channel: this.channel,
          first: SEARCH_RESULTS_PAGE_SIZE,
          search: this.search,
        }
      },
      result({ data }) {
        if (data) {
          this.queue = data.queue
          if (this.search) {
            this.publications = data.publications.edges.map(edge => edge.node)
          }
        }
      },
    },
  },
}
</script>

<template>
  <div class="container">
    <queue-manager
      :publications="queue"
      @move-up="moveUpInQueue"
      @move-down="moveDownInQueue"
      @remove="removeFromQueue"
    />
    <hr class="mt-5 mb-5 text-blue" />
    <input
      class="bg-transparent color-white w-full p-2 pl-6 pb-3 font-light text-3xl primary-search"
      placeholder="Search for..."
      :value="searchInput"
      @input="handleChange"
    />
    <div class="m-4">
      <simple-publications
        :publications="publications"
        @append="appendToQueue"
      />
    </div>
  </div>
</template>

<style scoped>
.primary-search {
  outline-style: none !important;
  box-shadow: none !important;
  border-color: transparent !important;
  background-color: #fff;

  &::placeholder {
    color: #000;
    /* color: red; */
  }
}
</style>
