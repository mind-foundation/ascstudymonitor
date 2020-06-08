<template>
  <div
    class="top-bar"
    :class="{
      focussed: isFocussed,
    }"
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
        @blur="isFocussed = false"
        type="text"
        class="title-bar__input"
        placeholder="Search.."
        role="search"
        ref="input"
      />

      <p class="typer" v-else @click="activate">
        Search For
        <vue-typer
          :text="texts"
          pre-type-delay="100"
          type-delay="120"
          pre-erase-delay="1500"
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

  data: () => ({
    activated: false,
    isFocussed: false,
    debounce: null,
    texts: ['Articles', 'Publications', 'Disciplines'],
  }),

  methods: {
    activate() {
      this.activated = true
      setTimeout(() => {
        this.$refs.input.focus()
      })
    },
    debounceSearch(e) {
      clearTimeout(this.debounce)
      this.debounce = setTimeout(() => {
        if (this.$store.state.route.query.search !== e.target.value) {
          this.$router.replace({
            query: {
              search: e.target.value,
            },
          })
        }
      }, 100)
    },
  },
}
</script>
<style lang="less">
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

  -webkit-transition: border-color 0.25s ease-in-out, -webkit-box-shadow 0.5s;
  transition: border-color 0.25s ease-in-out, -webkit-box-shadow 0.5s;
  transition: box-shadow 0.5s, border-color 0.25s ease-in-out;
  transition: box-shadow 0.5s, border-color 0.25s ease-in-out,
    -webkit-box-shadow 0.5s;

  &.focussed {
    outline: none;
    border: none;
    box-shadow: none;
    border-bottom: solid 1px #34557f;
  }
}

.title-bar {
  background-color: #fff;
  display: flex;
  justify-content: center;
  align-items: stretch;
  margin: 0 !important;
  padding: 0 !important;
}

.typer {
  position: absolute;
  left: 33px;
  top: 16px;
  font-size: 2em;
  cursor: pointer;
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
  padding: 10px 0 9px 32px;
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
}

.title-bar__input:focus {
  outline: none;
  border: none;
  box-shadow: none;
}

.title-bar__input::placeholder {
  color: #333;
  opacity: 0.75;
  font-weight: 300 !important;
  letter-spacing: 0;
}

.title-bar__input .data-table {
  font-size: 12px;
}

#ascSearch {
  padding: 0px 5px;
  margin: 0;
  height: 30px;
  width: 100%;
  font-size: 17px;
}

.vue-typer {
  cursor: pointer !important;

  .char {
    color: #333333 !important;
    opacity: 0.8;
  }
  .caret {
    margin-left: 3px;
  }
}
</style>
