<template>
  <div id="mindblower" ref="mindblower">
    <div id="mindblower__effect-container" v-html="mindBlowerHTML" />
    <div class="mindblower__label" aria-busy="true" role="alert"></div>
  </div>
</template>

<script lang="ts">
export default {
  name: 'mindblower',
  data: () => ({
    mindBlowerHTML: '',
  }),
  mounted() {
    this.mindBlowerHTML = (function() {
      let circles = ''
      const total = 80 // number of overlapping circles
      const size = 1200 // diameter of circles (px)

      const top = index =>
        -(size / 2) + (size / 2) * Math.cos((2 * Math.PI * (index - 1)) / total)

      const left = index =>
        -(size / 2) + (size / 2) * Math.sin((2 * Math.PI * (index - 1)) / total)

      for (
        let i = 1, end = total, asc = 1 <= end;
        asc ? i <= end : i >= end;
        asc ? i++ : i--
      ) {
        circles += `<div class="mindblower__circle index-${i}" style=" \
      width:${size}px; 
      height:${size}px; 
      top:${top(i)}px; 
      left:${left(i)}px; 
    "></div>`
      }

      return circles
    })()
  },
}
</script>

<style lang="less">
#mindblower {
  position: fixed;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
  background: #fff;
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

#mindblower__effect-container {
  width: 0;
  height: 0;
  position: absolute;
  top: 50%;
  left: 50%;
  -webkit-animation: spiral 60s infinite;
  animation: spiral 60s infinite;

  -webkit-transform: translateZ(0);
  -moz-transform: translateZ(0);
  -ms-transform: translateZ(0);
  -o-transform: translateZ(0);
  transform: translateZ(0);

  will-change: transform;
}

.mindblower__circle {
  border-top-left-radius: 50%;
  border-top-right-radius: 50%;
  border-bottom-right-radius: 50%;
  border-bottom-left-radius: 50%;
  border: 1px solid #ccc;
  position: absolute;
}

.mindblower__label {
  font-style: italic;
  color: #fff;
  backdrop-filter: blur(2px);
  width: 50px;
  height: 50px;
  border-radius: 40px;
  font-size: 1.15em;
  background: #34557f;
  line-height: 0.8em;
  z-index: 10;
  display: flex;
  justify-content: center;
  align-items: center;
  animation: grow 60s infinite;
  will-change: transform;
}

@-webkit-keyframes spiral {
  0% {
    opacity: 0;
    -webkit-transform: rotateZ(0deg);
  }
  2% {
    opacity: 1;
  }
  100% {
    -webkit-transform: rotateZ(360deg);
  }
}
@keyframes spiral {
  0% {
    opacity: 0;
    transform: rotateZ(0deg);
  }
  2% {
    opacity: 1;
  }
  100% {
    transform: rotateZ(360deg);
  }
}

@keyframes rotating {
  100% {
    transform: rotate(360deg);
  }
}

@keyframes grow {
  0% {
    opacity: 0;
    transform: scaleX(1);
  }
  2% {
    opacity: 1;
  }
  50% {
    transform: scale(6);
  }
  100% {
    transform: scale(1);
  }
}

@-webkit-keyframes grow {
  0% {
    opacity: 0;
    transform: scaleX(1);
  }
  2% {
    opacity: 1;
  }
  50% {
    transform: scale(3);
  }
  100% {
    transform: scale(1);
  }
}
</style>
