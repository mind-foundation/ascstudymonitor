<template>
  <div>
    <div>
      <t-input />
    </div>
    <div class="bg-white">Results</div>
  </div>
</template>

<script>
export default {
  name: 'search-widget',
  // props: ['publication'],
  // methods: {
  //   linkFor(network) {
  //     return (
  //       'https://asc-studymonitor.mind-foundation.org/p/' +
  //       this.publication.slug +
  //       '?utm_source=' +
  //       network +
  //       '&utm_medium=share_publication&utm_campaign=' +
  //       window.COMMIT_HASH
  //     )
  //   },
  //   trackShare(channel) {
  //     window.analytics.track('Publication shared', {
  //       channel,
  //     })
  //   },
  //   doCopy() {
  //     this.trackShare('copy')
  //     this.$copyText(this.linkFor('copy')).then(
  //       () => {
  //         this.$toasted.success('Link copied to clipboard', {
  //           className: 'radu-make-me-pretty-please',
  //           theme: 'toasted-primary',
  //           position: 'top-right',
  //           duration: 3000,
  //         })
  //       },
  //       () => {
  //         this.$toasted.show('hello billo XX')
  //       },
  //     )
  //   },
  // },
  // computed: {
  //   params() {
  //     return {
  //       title: this.publication.title,
  //       description: this.publication.abstract,
  //       quote: 'I’m a quote',
  //       hashtags: 'hashy,hash,hash2020,hash4you',
  //     }
  //   },
  // },
}
</script>

<style lang="less">
#search-widget {
  display: inline-flex;

  svg {
    vertical-align: bottom;
    transform: translateY(2px);
    zoom: 0.9;

    path {
      height: 20px;
      fill: #34557f;
    }
  }

  a {
    color: #34557f;
    font-weight: bold;

    &:hover {
      color: #607a9b;

      svg {
        transform: translateY(2px);

        path {
          fill: #607a9b;
        }
      }
    }
  }

  .copy-wrap {
    color: #34557f;
    font-weight: bold;
    cursor: pointer;

    svg {
      height: 24px;
      width: 24px;
    }

    &:hover {
      color: #607a9b;

      svg {
        transform: translateY(2px);

        path {
          fill: #607a9b;
        }
      }
    }
  }
}

.segment {
  margin: 0 10px;

  a,
  div > {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
  }
}

.radu-make-me-pretty-please {
  background-color: #c31d1d !important;
}
</style>
