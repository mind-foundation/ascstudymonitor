import { shallowMount, createLocalVue } from '@vue/test-utils'
import Vuex from 'vuex'
import List from '@/views/List.vue'

const localVue = createLocalVue()
localVue.use(Vuex)

describe('List.vue', () => {
  let store

  beforeEach(() => {
    store = new Vuex.Store({
      state: {
        route: {
          query: {},
        },
        publications: [
          {
            id: 'A',
            slug: '123456-A',
            websites: ['http://test.com'],
          },
        ],
      },
      getters: {
        queryPublications: () => [],
      },
    })
  })

  it('matches snapshot', () => {
    const wrapper = shallowMount(List, { store, localVue })
    expect(wrapper.element).toMatchSnapshot()
  })

  it('renders the entry', () => {
    const wrapper = shallowMount(List, { store, localVue })
    expect(wrapper.find('#list').exists()).toBe(true)
  })
})
