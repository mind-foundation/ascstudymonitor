import { shallowMount } from '@vue/test-utils'
import FilterModal from '@/components/FilterModal.vue'

describe('FilterModal.vue', () => {
  let store

  it('renders', () => {
    const wrapper = shallowMount(FilterModal, { store })
    expect(wrapper.find('.modal-container').exists()).toBe(true)
  })
})
