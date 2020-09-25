<script>
import LinkIcon from '@/components/Icons/Link.vue'
import ShareIcon from '@/components/Icons/Share.vue'
export default {
  name: 'links',
  props: {
    publication: {
      type: Object,
      required: true,
    },
  },
  components: {
    LinkIcon,
    ShareIcon,
  },
}
</script>
<template>
  <div class="flex-row justify-start">
    <div
      class="inline-flex"
      v-for="website in publication.websites"
      v-bind:key="website"
    >
      <a target="_blank" rel="noopener noreferrer" :href="website">
        <div class="icon-holder">
          <link-icon />
        </div>
        Visit publisher website
      </a>
    </div>

    <div class="inline-flex" v-if="publication.fileAttached">
      <download-icon big="false" />
      <a
        target="_blank"
        rel="noopener noreferrer"
        :href="$api + '/p/' + publication.slug + '/download'"
      >
        Download full text
      </a>
    </div>
    <div class="inline-flex">
      <a
        target="_blank"
        rel="noopener noreferrer"
        :href="$api + '/p/' + publication.slug + '/download'"
      >
        <div class="icon-holder">
          <share-icon />
        </div>

        Get Link to Post
      </a>
    </div>
  </div>
</template>

<style lang="less" scoped>
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
  display: inline-block;
}
</style>
