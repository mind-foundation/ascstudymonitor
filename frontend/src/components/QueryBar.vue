<template>
  <div class="top-bar" data-sticky-container>
    <div
      class="title-bar"
      data-sticky
      data-options="marginTop:0;"
      style="width:100%"
    >
      <input
        @input="debounceSearch($event)"
        type="text"
        class="title-bar__input"
        placeholder="Search all articles..."
        role="search"
      />
    </div>
  </div>
</template>

<script>
export default {
  name: 'query-bar',

  data: () => ({
    debounce: null,
  }),

  methods: {
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
}

.title-bar {
  background-color: #fff;
  display: flex;
  justify-content: center;
  align-items: stretch;
  margin: 0 !important;
  padding: 0 !important;
}

.title-bar__input {
  border: none;
  border-bottom: solid 1px #e0e0e0;
  background: transparent;
  outline: none;
  color: #333333;
  box-sizing: content-box;
  font-weight: 300;
  letter-spacing: 0;
  display: block;
  font-size: inherit;
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
  border-bottom: solid 1px #34557f;
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
</style>
