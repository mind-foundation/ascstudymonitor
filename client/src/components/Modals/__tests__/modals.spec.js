import { shallowMount, createLocalVue } from '@vue/test-utils'
import Donate from '../Donate'
import About from '../About'
import VueModal from 'vue-js-modal'

describe('Modals', () => {
  var localVue

  beforeEach(() => {
    localVue = createLocalVue()
    localVue.use(VueModal)
  })

  describe('Donate', () => {
    it('renders', () => {
      const wrapper = shallowMount(Donate, { localVue })
      expect(wrapper.find('.modal-container').isVisible()).toBe(true)
    })
  })

  describe('About.vue', () => {
    it('renders', () => {
      const wrapper = shallowMount(About, { localVue })
      expect(wrapper.find('.modal-container').exists()).toBe(true)
    })
  })
})
