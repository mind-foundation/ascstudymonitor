<script>
export default {
  name: 'icon-download',
}
</script>
<template>
  <div class="entry__downloads-item" big>
    <div class="entry__downloads-icon entry__downloads-icon__blue">
      <svg
        xmlns="http://www.w3.org/2000/svg"
        width="14.847"
        height="16.271"
        viewBox="0 0 14.847 16.271"
      >
        <g transform="translate(-1375.217 -461.318)">
          <path
            class="asc_download_ico"
            d="M1391.141,3120.591h-4.424v12.621h13.847v-12.621h-4.786"
            transform="translate(-11 -2656.124)"
          />
          <g transform="translate(1379.459 461.318)">
            <path
              class="asc_download_ico"
              d="M1391.605,3117.109l3.082,3.012,3.082-3.012"
              transform="translate(-1391.605 -3107.066)"
            />
            <path
              class="asc_download_ico"
              d="M1396.051,3105.522v13.247"
              transform="translate(-1392.973 -3105.522)"
            />
          </g>
        </g>
      </svg>
    </div>
  </div>
</template>

<style lang="less" scoped>
.entry__downloads-item {
  margin-right: 24px;
  display: inline-flex;
  flex-direction: row;
  align-items: center;
  justify-content: stretch;
}

.entry__downloads-item .entry__icon {
  position: relative;
  bottom: -3px;
  left: 5px;
}

.entry__downloads-item .entry__icon svg {
  height: 20px;
}

.asc_download_ico {
  fill: none;
  stroke: #fff;
}
</style>
