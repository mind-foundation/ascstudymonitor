<script>
export default {
  name: 'top-navigation',
}
</script>

<template>
  <div class="container flex flex-row-reverse mt-6">
    <t-button variant="cta" tabindex="-1" @click="$modal.show('donate-modal')">
      DONATE
    </t-button>

    <t-button
      variant="transparent"
      tabindex="-1"
      @click="$modal.show('about-modal')"
    >
      ABOUT
    </t-button>
  </div>
</template>

<style scoped>
.container button {
  letter-spacing: 2px;
}
</style>
