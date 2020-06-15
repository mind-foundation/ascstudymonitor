<template>
  <div
    class="top-bar"
    :class="{
      focussed: isFocussed,
      mobileBarActivated: $store.state.mobileBarActivated,
    }"
    @click="activate"
  >
    <div
      class="title-bar"
      data-sticky
      data-options="marginTop:0;"
      style="width:100%"
    >
      <input
        v-if="activated"
        @input="debounceSearch($event)"
        @focus="isFocussed = true"
        @blur="onBlur($event)"
        :value="query"
        type="text"
        class="title-bar__input"
        placeholder="Search All Articles..."
        role="search"
        ref="input"
      />

      <p class="typer" v-else>
        Search For
        <vue-typer
          :text="texts"
          erase-style="clear"
          caret-animation="blink"
          :pre-type-delay="200"
          :type-delay="140"
          :pre-erase-delay="1500"
        ></vue-typer>
      </p>
    </div>
  </div>
</template>

<script>
import { VueTyper } from 'vue-typer'

export default {
  name: 'query-bar',
  components: {
    VueTyper,
  },
  data() {
    const paramQuery = this.$store.state.route.query?.search
    const query = paramQuery ? paramQuery.replace(/\+/g, ' ') : ''
    return {
      query,
      activated: Boolean(query),
      isFocussed: false,
      debounce: null,
      texts: ['Titles', 'Authors', 'Journals', 'Keywords', 'Disciplines'],
    }
  },

  methods: {
    activate() {
      this.activated = true
      setTimeout(() => {
        this.$refs.input.focus()
      })
    },
    onBlur(e) {
      this.isFocussed = false
      if (!e.target.value) {
        this.activated = false
      }
    },
    debounceSearch(e) {
      this.query = e.target.value

      clearTimeout(this.debounce)
      this.debounce = setTimeout(() => {
        if (this.$store.state.route.query.search !== e.target.value) {
          this.$router.replace({
            query: {
              ...this.$store.state.route.query,
              search: e.target.value.replace(/\s/g, '+'),
            },
          })
        }
      }, 300)
    },
  },
}
</script>
<style lang="less">
@import "~@/styles/variables";

.top-bar {
  padding: 0 !important;
  height: 70px;
  top: 0;
  position: fixed;
  left: 240px;
  width: calc(100vw - 240px);
  background: #fff;
  z-index: 1;
  border-bottom: solid 1px #e0e0e0;
  cursor: text;

  -webkit-transition: border-color 0.25s ease-in-out, -webkit-box-shadow 0.5s;
  transition: border-color 0.25s ease-in-out, -webkit-box-shadow 0.5s;
  transition: box-shadow 0.5s, border-color 0.25s ease-in-out;
  transition: box-shadow 0.5s, border-color 0.25s ease-in-out,
    -webkit-box-shadow 0.5s;

  @media @for-phone {
    top: @mobile-header-height;
    left: 0;
    height: 30px;
    width: 100%;
    border-bottom: solid 3px @primary;
    transform: translateY(-30px);
    transition: all 0.1s ease-in-out;
    opacity: 0;
  }

  &.mobileBarActivated {
    transform: translateY(0px);
    opacity: 1;
  }

  &.focussed {
    outline: none;
    border: none;
    box-shadow: none;
    border-bottom: solid 1px #34557f;

    @media @for-phone {
      border-bottom: solid 3px @primary;
    }
  }
}

.title-bar {
  background-color: #fff;
  display: flex;
  justify-content: center;
  font-weight: 300;
  align-items: stretch;
  margin: 0 !important;
  padding: 0 !important;
}

.typer {
  position: absolute;
  left: 32px;
  bottom: -0.5px;
  font-size: 2em;
  margin-bottom: 0px;

  @media @for-phone {
    font-size: 1em;
  }

}

.title-bar__input {
  display: none;
  border: none;

  background: transparent;
  outline: none;
  color: #333333;
  box-sizing: content-box;
  font-weight: 300;
  letter-spacing: 0;
  display: block;
  font-size: 2em;
  font-weight: 300 !important;
  margin: 0;
  height: 50px;
  appearance: none;
  -webkit-appearance: none;
  box-shadow: none;
  max-width: inherit !important;
  margin-right: inherit !important;
  margin: 0 !important;
  width: 100%;
  font-family: 'Open Sans', sans-serif !important;
  padding: 10px 0 9px 32px;

  @media @for-phone {
    padding: 2px 20px;
    height: 20px;
    font-size: 1em;
  }
}

.title-bar__input:focus {
  outline: none;
  border: none;
  box-shadow: none;
}

.title-bar__input::placeholder {
  color: #333;
  opacity: 0.75;
  letter-spacing: 0;
}

.vue-typer {
  cursor: text !important;

  .char {
    color: #333333 !important;
    opacity: 0.8;
  }
  .caret {
    margin-left: 3px;
  }
}
</style>
