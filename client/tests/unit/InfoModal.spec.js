import { shallowMount } from '@vue/test-utils'
import InfoModal from '@/components/InfoModal.vue'

describe('InfoModal.vue', () => {
  let store

  it('renders', () => {
    const wrapper = shallowMount(InfoModal, { store })
    expect(wrapper.find('.modal-container').exists()).toBe(true)
  })
})
