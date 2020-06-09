import { shallowMount } from '@vue/test-utils'
import Mindblower from '@/components/Mindblower.vue'

describe('Mindblower.vue', () => {
  it('matches snapshot', () => {
    const wrapper = shallowMount(Mindblower, {})
    expect(wrapper.element).toMatchSnapshot()
  })

  it('renders the container', () => {
    const wrapper = shallowMount(Mindblower, {})
    expect(wrapper.find('#mindblower').exists()).toBe(true)
  })
})
