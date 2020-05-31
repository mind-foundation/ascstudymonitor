<script>
export default {
  name: 'icon-science',
}
</script>
<template>
  <div class="entry__icon">
    <svg
      xmlns="http://www.w3.org/2000/svg"
      width="25"
      height="25"
      viewBox="0 0 25 25"
    >
      <g transform="translate(-67.156 -347.19)">
        <g class="a4" transform="translate(81.6 360.2)">
          <circle class="a4" cx="5.5" cy="5.5" r="5.5" />
        </g>
        <g class="a4" transform="translate(68.156 348)">
          <rect class="a4" width="9.5" height="9.5" />
        </g>
        <g class="a4" transform="translate(67.156 360.19)">
          <path class="a4" d="M6.5,0,13,11H0Z" />
        </g>
        <line
          class="a4"
          x2="9.085"
          y2="9.085"
          transform="translate(82.628 347.757)"
        />
        <line
          class="a4"
          x2="9.085"
          y2="9.085"
          transform="translate(91.713 347.757) rotate(90)"
        />
      </g>
    </svg>
  </div>
</template>

<style lang="less" scoped>
.filter_header__svg_a,
.filter_header__svg_d {
  fill: #fff;
}
.filter_header__svg_a,
.filter_header__svg_b {
  stroke: #fff;
}
.filter_header__svg_b {
  fill: #fff;
}
.filter_header__svg_c {
  stroke: none;
}

.entry__icon .l {
  fill: none;
  stroke: #333;
  stroke-width: 1px;
}

.entry__disciplines {
  list-style: none;
  padding-bottom: 10px;
}
.entry__disciplines a {
  color: #34557f;
  font-size: 1.2em;
  font-weight: 700;
  margin-right: 8px;
}

.entry__icon {
  width: 32px;
  min-width: 32px;
}

.entry__disciplines svg {
  height: 20px;
  position: relative;
  bottom: -5px;
  left: 0.05em;
}

.entry__disciplines svg .a4 {
  fill: none;
  stroke: #34557f;
  stroke-width: 1px;
}
</style>
