import { shallowMount, createLocalVue } from '@vue/test-utils'
import Vuex from 'vuex'
import QueryBar from '@/components/QueryBar.vue'

const localVue = createLocalVue()
localVue.use(Vuex)

describe('QuerBar.vue', () => {
  let store

  beforeEach(() => {
    store = new Vuex.Store({
      state: {
        route: {
          query: {},
        },
      },
    })
  })

  it('matches snapshot', () => {
    const wrapper = shallowMount(QueryBar, { store, localVue })
    expect(wrapper.element).toMatchSnapshot()
  })

  it('renders the bar', () => {
    const wrapper = shallowMount(QueryBar, { store, localVue })
    expect(wrapper.find('.top-bar').exists()).toBe(true)
  })
})
