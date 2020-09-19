<script>
export default {
  name: 'top-navigation',
}
</script>

<template>
  <div class="container flex flex-row-reverse mt-6">
    <button
      class="pt-3 pb-3 pl-8 pr-8 leading-none bg-navy bg-transparent text-white text-xs"
      tabindex="-1"
      @click="$modal.show('donate-modal')"
    >
      DONATE
    </button>

    <button
      class="pt-3 pb-3 pl-8 pr-8 leading-none border-transparent bg-transparent text-xs"
      tabindex="-1"
      @click="$modal.show('about-modal')"
    >
      ABOUT
    </button>
  </div>
</template>

<style scoped>
.container button {
  letter-spacing: 2px;
}
</style>
