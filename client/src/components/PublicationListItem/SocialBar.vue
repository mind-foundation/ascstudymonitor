<template>
  <div id="social-bar">
    <div class="segment">
      <ShareNetwork
        network="email"
        :url="linkFor('email')"
        :title="params.title"
        :description="params.description"
        :quote="params.quote"
        :hashtags="params.hashtags"
        @click="trackShare('email')"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="24"
          height="24"
          viewBox="0 0 24 24"
        >
          <path
            d="M12 2.02c5.514 0 10 4.486 10 10s-4.486 10-10 10-10-4.486-10-10 4.486-10 10-10zm0-2c-6.627 0-12 5.373-12 12s5.373 12 12 12 12-5.373 12-12-5.373-12-12-12zm0 12.55l-5.992-4.57h11.983l-5.991 4.57zm0 1.288l-6-4.629v6.771h12v-6.771l-6 4.629z"
          />
        </svg>
        Email
      </ShareNetwork>
    </div>
    <div class="segment">
      <ShareNetwork
        network="twitter"
        :url="linkFor('twitter')"
        :title="params.title"
        :description="params.description"
        :quote="params.quote"
        :hashtags="params.hashtags"
        @click="trackShare('twitter')"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="24"
          height="24"
          viewBox="0 0 24 24"
        >
          <path
            d="M12 2c5.514 0 10 4.486 10 10s-4.486 10-10 10-10-4.486-10-10 4.486-10 10-10zm0-2c-6.627 0-12 5.373-12 12s5.373 12 12 12 12-5.373 12-12-5.373-12-12-12zm6.5 8.778c-.441.196-.916.328-1.414.388.509-.305.898-.787 1.083-1.362-.476.282-1.003.487-1.564.597-.448-.479-1.089-.778-1.796-.778-1.59 0-2.758 1.483-2.399 3.023-2.045-.103-3.86-1.083-5.074-2.572-.645 1.106-.334 2.554.762 3.287-.403-.013-.782-.124-1.114-.308-.027 1.14.791 2.207 1.975 2.445-.346.094-.726.116-1.112.042.313.978 1.224 1.689 2.3 1.709-1.037.812-2.34 1.175-3.647 1.021 1.09.699 2.383 1.106 3.773 1.106 4.572 0 7.154-3.861 6.998-7.324.482-.346.899-.78 1.229-1.274z"
          />
        </svg>
        Twitter
      </ShareNetwork>
    </div>
    <div class="segment">
      <ShareNetwork
        network="telegram"
        :url="linkFor('telegram')"
        :title="params.title"
        :description="params.description"
        :quote="params.quote"
        :hashtags="params.hashtags"
        @click="trackShare('telegram')"
      >
        <svg
          width="24px"
          height="24px"
          version="1.1"
          xmlns="http://www.w3.org/2000/svg"
          xmlns:xlink="http://www.w3.org/1999/xlink"
          xml:space="preserve"
          xmlns:serif="http://www.serif.com/"
          style="fill-rule:evenodd;clip-rule:evenodd;stroke-linejoin:round;stroke-miterlimit:1.41421;"
        >
          <path
            id="telegram-5"
            d="M12,0c-6.627,0 -12,5.373 -12,12c0,6.627 5.373,12 12,12c6.627,0 12,-5.373 12,-12c0,-6.627 -5.373,-12 -12,-12Zm0,2c5.514,0 10,4.486 10,10c0,5.514 -4.486,10 -10,10c-5.514,0 -10,-4.486 -10,-10c0,-5.514 4.486,-10 10,-10Zm2.692,14.889c0.161,0.115 0.368,0.143 0.553,0.073c0.185,-0.07 0.322,-0.228 0.362,-0.42c0.435,-2.042 1.489,-7.211 1.884,-9.068c0.03,-0.14 -0.019,-0.285 -0.129,-0.379c-0.11,-0.093 -0.263,-0.12 -0.399,-0.07c-2.096,0.776 -8.553,3.198 -11.192,4.175c-0.168,0.062 -0.277,0.223 -0.271,0.4c0.006,0.177 0.125,0.33 0.296,0.381c1.184,0.354 2.738,0.847 2.738,0.847c0,0 0.725,2.193 1.104,3.308c0.047,0.139 0.157,0.25 0.301,0.287c0.145,0.038 0.298,-0.001 0.406,-0.103c0.608,-0.574 1.548,-1.461 1.548,-1.461c0,0 1.786,1.309 2.799,2.03Zm-5.505,-4.338l0.84,2.769l0.186,-1.754c0,0 3.243,-2.925 5.092,-4.593c0.055,-0.048 0.062,-0.13 0.017,-0.188c-0.045,-0.057 -0.126,-0.071 -0.188,-0.032c-2.143,1.368 -5.947,3.798 -5.947,3.798Z"
          />
        </svg>
        Telegram
      </ShareNetwork>
    </div>
    <div class="segment">
      <div class="copy-wrap" @click="doCopy()">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
          <path
            d="M15.143 13.244l.837-2.244 2.698 5.641-5.678 2.502.805-2.23s-8.055-3.538-7.708-10.913c2.715 5.938 9.046 7.244 9.046 7.244zm8.857-7.244v18h-18v-6h-6v-18h18v6h6zm-2 2h-12.112c-.562-.578-1.08-1.243-1.521-2h7.633v-4h-14v14h4v-3.124c.6.961 1.287 1.823 2 2.576v6.548h14v-14z"
          />
        </svg>
        Copy
      </div>
    </div>
  </div>
</template>

<script>
/**
 * Thanks https://iconmonstr.com/ for providing
 * icons for non-commercial projects free of charge
 */
export default {
  name: 'social-bar',
  props: ['publication'],
  methods: {
    linkFor(network) {
      return (
        `${location.protocol}//${location.host}/p/` +
        this.publication.slug +
        '?utm_source=' +
        network +
        '&utm_medium=share_publication&utm_campaign=' +
        window.COMMIT_HASH
      )
    },
    trackShare(channel) {
      window.analytics.track('Publication shared', {
        channel,
      })
    },
    doCopy() {
      this.trackShare('copy')
      this.$copyText(this.linkFor('copy')).then(
        () => {
          this.$toasted.success('Link copied to clipboard', {
            className: 'radu-make-me-pretty-please',
            theme: 'toasted-primary',
            position: 'top-right',
            duration: 3000,
          })
        },
        () => {
          this.$toasted.show('hello billo XX')
        },
      )
    },
  },
  computed: {
    params() {
      return {
        title: this.publication.title,
        description: this.publication.abstract,
        quote: 'I’m a quote',
        hashtags: 'hashy,hash,hash2020,hash4you',
      }
    },
  },
}
</script>

<style>
#social-bar {
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
