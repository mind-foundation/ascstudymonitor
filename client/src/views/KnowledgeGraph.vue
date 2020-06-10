<template>
  <div>
    <div class="node-info">
      <ul>
        <li>
          <!-- <a :href="this.url(this.selected)"> -->
          {{ this.selected.name }} : {{ this.selected.keywords.join(' ') }}
          <!-- </a> -->
        </li>
        <li>
          <!-- <a :href="this.url(this.selectedNeighbour[0])"> -->
          {{ this.selectedNeighbours[0].name }} :
          {{ this.selectedNeighbours[0].keywords.join(' ') }}
          <!-- </a> -->
        </li>
        <li>
          <!-- <a :href="this.url(this.selectedNeighbour[1])"> -->
          {{ this.selectedNeighbours[1].name }} :
          {{ this.selectedNeighbours[1].keywords.join(' ') }}
          <!-- </a> -->
        </li>
      </ul>
    </div>
    <d3-network
      ref="net"
      @node-click="selectNode"
      :net-nodes="nodes"
      :net-links="links"
      :options="options"
    />
  </div>
</template>
<script>
import D3Network from 'vue-d3-network'
import * as graph from '../graph.json'

export default {
  name: 'KnowledgeGraph',
  components: { D3Network },
  data: () => {
    const { nodes, links } = graph
    const idToNode = nodes.reduce(
      (bag, node) => ({ ...bag, [node.id]: node }),
      {},
    )
    const recommendations = nodes.reduce(
      (bag, node) => ({
        ...bag,
        [node.id]: links.filter(l => l.sid == node.id).map(l => l.tid),
      }),
      {},
    )
    const selected = nodes[0]
    return { nodes, links, idToNode, recommendations, selected }
  },
  computed: {
    options() {
      return {
        force: 100,
        size: { h: 1024 },
        nodeSize: 15,
        linkWidth: 5,
        nodeLabels: false,
        linkLabels: false,
        canvas: false,
        linkWidth: 2,
      }
    },
    selectedNeighbours() {
      return this.recommendations[this.selected.id].map(id => this.idToNode[id])
    },
  },
  methods: {
    url: node => {
      return `http://localhost:8080/p/${node.id}`
    },
    selectNode(event, node) {
      this.selected = node
    },
  },
}
</script>
<style>
.link {
  stroke: #000;
}
</style>
