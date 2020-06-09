import { shallowMount } from '@vue/test-utils'
import MindBlower from '@/components/MindBlower.vue'

describe('Mindblower.vue', () => {
  it('matches snapshot', () => {
    const wrapper = shallowMount(MindBlower, {})
    expect(wrapper.element).toMatchSnapshot()
  })

  it('renders the container', () => {
    const wrapper = shallowMount(MindBlower, {})
    expect(wrapper.find('#mindblower').exists()).toBe(true)
  })
})
