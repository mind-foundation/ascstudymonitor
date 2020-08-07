<script>
export default {
  name: 'info-modal',
}
</script>

<template>
  <modal name="filter-modal">
    <div class="modal-container reveal">
      <h3>Woop woop I’m a modal</h3>

      <div class="modal-body">
        <p>
          Felix doesn’t like me but Radu is gonna pull off a stunt.
        </p>
        <div>
          <a href="#">
            Pew pew
          </a>
        </div>
      </div>
    </div>
  </modal>
</template>

<style lang="less">
.modal-container {
  margin: 0px auto;
  background-color: #fefefe;
  border-radius: 2px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.33);
  transition: all 0.3s ease;
  text-align: left;
  padding: 30px 45px;
  position: relative;
  outline: none;
  height: 100%;

  h3 {
    text-align: left;
    font-weight: 300;
  }

  p {
    margin: 0;
    text-align: left;
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

.modal-body {
  margin: 10px 0;
}

.modal-default-button {
  float: right;
}
</style>
