import { shallowMount, createLocalVue } from '@vue/test-utils'
import About from '../About'
import VueModal from 'vue-js-modal'

describe('Modals', () => {
  var localVue

  beforeEach(() => {
    localVue = createLocalVue()
    localVue.use(VueModal)
  })

  describe('About.vue', () => {
    it('renders', () => {
      const wrapper = shallowMount(About, { localVue })
      expect(wrapper.find('.modal-container').exists()).toBe(true)
    })
  })
})
