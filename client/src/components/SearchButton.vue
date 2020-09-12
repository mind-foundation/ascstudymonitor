<script>
export default {
  name: 'search-button',
}
</script>

<template>
  <div class="relative">
    <t-button
      @click="$modal.show('search-modal')"
      classes="bg-blue pt-3 pb-3 pl-20 pr-20 text-white color-red font-bold text-sm"
    >
      <svg
        xmlns="http://www.w3.org/2000/svg"
        width="25.161"
        height="24.947"
        viewBox="0 0 25.161 24.947"
        class="search inline-block mr-3"
      >
        <g transform="translate(-659.798 -324.826)">
          <g
            transform="translate(659.798 324.826)"
            fill="none"
            stroke="#c4d5e0"
            stroke-width="2"
          >
            <circle cx="9" cy="9" r="9" stroke="none" />
            <circle cx="9" cy="9" r="8" fill="none" />
          </g>
          <path
            d="M694.109,2868.172l8.965,8.709"
            transform="translate(-18.812 -2527.826)"
            fill="none"
            stroke="#c4d5e0"
            stroke-width="2"
          />
        </g>
      </svg>
      Search and Filter all Publications</t-button
    >
  </div>
</template>

<style lang="less">
.search {
  position: relative;
  top: -2px;
}
</style>
