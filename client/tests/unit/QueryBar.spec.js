import { shallowMount } from '@vue/test-utils'
import QueryBar from '@/components/QueryBar.vue'

describe('QueryBar.vue', () => {
  it('matches snapshot', () => {
    const wrapper = shallowMount(QueryBar, {})
    expect(wrapper.element).toMatchSnapshot()
  })

  it('renders the bar', () => {
    const wrapper = shallowMount(QueryBar, {})
    expect(wrapper.find('.top-bar').exists()).toBe(true)
  })
})
