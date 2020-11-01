<template>
  <div class="modal-mask">
    <div class="modal-wrapper">
      <div class="modal-container">
        <slot name="body">Put your custom body in the slot</slot>
      </div>
    </div>
  </div>
</template>

<script>
export default {}
</script>

<style scoped>
#app {
  padding: 1rem;
}

.modal-mask {
  position: fixed;
  z-index: 9998;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: table;
  /* transition: all 3s ease; */
  opacity: 1;
}

.modal-wrapper {
  display: table-cell;
  vertical-align: middle;
}

/* 
.modal-container {
  // implemented by individual modals!
} */

.modal-header h3 {
  margin-top: 0;
  color: #42b983;
}

.modal-default-button {
  display: block;
  margin-top: 1rem;
}

/* 
.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-leave-from,
.modal-enter-to {
  opacity: 1;
}

.modal-enter-from .modal-container,
.modal-leave-active .modal-container {
  -webkit-transform: scale(1.1);
  transform: scale(1.1);
} */
</style>
