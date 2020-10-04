<script>
export default {
  name: 'utiliy-button',
}
</script>

<template>
  <div class="align">
    <router-link to="/">
      <button
        class="bg-superwhite hover:bg-lightblue hover:text-white border-lightblue border-2 pt-3 pb-3 pl-16 pr-16 font-bold text-sm"
      >
        Publication index from the ASC Study Monitor
      </button>
    </router-link>
  </div>
</template>

<style scoped>
.align {
  position: absolute;
  height: 50px;
  left: 0;
  right: 0px;
  top: 0;
  transform: translateY(-25px);
  display: flex;
  justify-content: center;
  align-items: center;
}

button {
  transition: all 0.2s ease-in-out;
}
</style>
