import { shallowMount, createLocalVue } from '@vue/test-utils'
import Donate from '../Donate.vue'
import VueModal from 'vue-js-modal'

describe('Donate.vue', () => {
  let store

  const localVue = createLocalVue()
  localVue.use(VueModal)

  it('renders', () => {
    const wrapper = shallowMount(Donate, { store, localVue })
    expect(wrapper.find('.modal-container').exists()).toBe(true)
  })
})
