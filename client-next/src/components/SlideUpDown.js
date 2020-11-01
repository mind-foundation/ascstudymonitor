import { h } from 'vue'
// adapted for vue 3, based off:
// https://github.com/danieldiekmeier/vue-slide-up-down/blob/master/src/slide-up-down.js
/*
MIT License

Copyright (c) 2018 Daniel Diekmeier

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/
export default {
  name: 'SlideUpDown',

  props: {
    active: Boolean,
    duration: {
      type: Number,
      default: 500,
    },
    tag: {
      type: String,
      default: 'div',
    },
    useHidden: {
      type: Boolean,
      default: true,
    },
  },

  data: () => ({
    style: {},
    initial: false,
    hidden: false,
  }),

  watch: {
    active() {
      this.layout()
    },
  },

  setup(props, { attrs }) {
    return { attrs }
  },

  render() {
    return h(
      this.tag,
      {
        style: this.style,
        attrs: this.attrs,
        ref: 'container',
        on: { transitionend: this.onTransitionEnd },
      },
      this.$slots.default,
    )
  },

  mounted() {
    this.layout()
    this.initial = true
  },

  created() {
    this.hidden = !this.active
  },

  computed: {
    el() {
      return this.$refs.container
    },

    attrs() {
      const attrs = {
        'aria-hidden': !this.active,
        'aria-expanded': this.active,
      }

      if (this.useHidden) {
        attrs.hidden = this.hidden
      }

      return attrs
    },
  },

  methods: {
    layout() {
      if (this.active) {
        this.hidden = false
        // this.$emit('open-start')
        if (this.initial) {
          this.setHeight('0px', () => this.el.scrollHeight + 'px')
        }
      } else {
        // this.$emit('close-start')
        this.setHeight(this.el.scrollHeight + 'px', () => '0px')
      }
    },

    asap(callback) {
      if (!this.initial) {
        callback()
      } else {
        this.$nextTick(callback)
      }
    },

    setHeight(temp, afterRelayout) {
      this.style = { height: temp }

      this.asap(() => {
        // force relayout so the animation will run
        this.__ = this.el.scrollHeight

        this.style = {
          height: afterRelayout(),
          overflow: 'hidden',
          'transition-property': 'height',
          'transition-duration': this.duration + 'ms',
        }
      })
    },

    onTransitionEnd(event) {
      // Don't do anything if the transition doesn't belong to the container
      if (event.target !== this.el) return

      if (this.active) {
        this.style = {}
        // this.$emit('open-end')
      } else {
        this.style = {
          height: '0',
          overflow: 'hidden',
        }
        this.hidden = true
        // this.$emit('close-end')
      }
    },
  },
}
