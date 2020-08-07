<script>
export default {
  name: 'list-hero',
}
</script>

<template>
  <h1>Explore curated publications on altered state of consciousness</h1>
</template>

<style lang="less">
.modal-container {
  margin: 0px auto;
  background-color: #fefefe;
  border-radius: 2px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.33);
  transition: all 0.3s ease;

  h3 {
    margin-top: 0;
    color: #42b983;
    font-size: 1.9375rem;
  }
}

.modal-body {
  margin: 10px 0;
}

.modal-default-button {
  float: right;
}

.reveal {
  text-align: left;
  padding: 30px 45px;
  position: relative;
  outline: none;

  h3 {
    text-align: left;
    color: #333;
    font-weight: 300;
  }

  p {
    margin: 0;
    text-align: left;
    color: #333;
    line-height: 1.8;
    padding-bottom: 20px;
  }

  a {
    font-weight: 600;
    color: #fff;
    background: linear-gradient(to right, #1a9da4, #34557f);
    padding: 3px 20px;
    font-size: 15px;
    line-height: 3em;
    display: inline-block;
  }
}

.vm--modal {
  background: none !important;
}
</style>
