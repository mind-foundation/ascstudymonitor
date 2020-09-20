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
      this.$apollo.mutate({
        mutation: AppendToQueueMutation,
        variables: {
          channel: this.channel,
          publication: publication,
        },
      })
    },
    moveUpInQueue(publication) {
      this.$apollo.mutate({
        mutation: MoveUpInQueueMutation,
        variables: {
          channel: this.channel,
          publication: publication,
        },
      })
    },
    moveDownInQueue(publication) {
      this.$apollo.mutate({
        mutation: MoveDownInQueueMutation,
        variables: {
          channel: this.channel,
          publication: publication,
        },
      })
    },
    removeFromQueue(publication) {
      this.$apollo.mutate({
        mutation: RemoveFromQueueMutation,
        variables: {
          channel: this.channel,
          publication: publication,
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
          this.publications = data.publications.edges.map(edge => edge.node)
        }
      },
    },
  },
}
</script>

<template>
  <div id="queue" class="containe">
    <queue-manager
      :publications="queue"
      @move-up="moveUpInQueue"
      @move-down="moveDownInQueue"
      @remove="removeFromQueue"
    />
    <hr />
    <input
      class="bg-transparent color-white w-full p-2 pl-6 pb-3 font-light text-3xl"
      placeholder="Search for..."
      :value="searchInput"
      @input="handleChange"
    />
    <simple-publications :publications="publications" @append="appendToQueue" />
  </div>
</template>

<style lang="less"></style>
