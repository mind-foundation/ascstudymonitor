<template>
  <div id="app">
    <navigation />

    <main id="main">
      <query-bar />
      <router-view />
    </main>
    <!-- <mindblower /> -->
    <!-- <div id="nav">
      <router-link to="/">Home</router-link> |
      <router-link to="/about">About</router-link>
    </div> -->
  </div>
</template>

<script>
import Navigation from './components/Navigation'
import QueryBar from './components/QueryBar'
// import Mindblower from './components/Mindblower'

export default {
  components: {
    Navigation,
    QueryBar,
    // Mindblower,
  },
  created() {
    this.$store.dispatch('loadPublications')
  },
}
</script>
<style lang="less">
body {
  margin: 0;
  padding: 0;
  background: #fefefe;
  font-weight: 400;
  line-height: 1.5;
  color: #0a0a0a;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;

  color: #777;
  display: flex;
  flex-direction: row;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;

  font-family: 'Open Sans', sans-serif !important;
  font-size: 12px;
}
blockquote,
dd,
div,
dl,
dt,
form,
h1,
h2,
h3,
h4,
h5,
h6,
li,
ol,
p,
pre,
td,
th,
ul {
  margin: 0;
  margin-top: 0px;
  margin-right: 0px;
  margin-bottom: 0px;
  margin-left: 0px;
  padding: 0;
}
#main {
  margin-left: 240px;
  margin-top: 70px;
}

#nav {
  padding: 30px;

  a {
    font-weight: bold;
    color: #2c3e50;

    &.router-link-exact-active {
      color: #42b983;
    }
  }
}
</style>
