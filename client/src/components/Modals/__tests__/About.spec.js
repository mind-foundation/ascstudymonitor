import { shallowMount, createLocalVue } from '@vue/test-utils'
import About from '../About.vue'
import VueModal from 'vue-js-modal'

describe('About.vue', () => {
  let store

  const localVue = createLocalVue()
  localVue.use(VueModal)

  it('renders', () => {
    const wrapper = shallowMount(About, { store, localVue })
    expect(wrapper.find('.modal-container').exists()).toBe(true)
  })
})
