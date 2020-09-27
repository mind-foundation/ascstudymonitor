import { shallowMount, createLocalVue } from '@vue/test-utils'
import List from '../List.vue'

const localVue = createLocalVue()

describe('List.vue', () => {
  it('renders the entry', () => {
    const wrapper = shallowMount(List, {
      localVue,
      mocks: { $constants: { PAGE_SIZE: 10 } },
    })
    expect(wrapper.find('#list').exists()).toBe(true)
  })
})
