import { shallowMount, createLocalVue } from '@vue/test-utils'
import Vuex from 'vuex'
import List from '../List.vue'

const localVue = createLocalVue()
localVue.use(Vuex)

describe('List.vue', () => {
  let store

  beforeEach(() => {
    store = new Vuex.Store({
      modules: {
        publications: {
          namespaced: true,
          state: {
            items: [
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
        },
      },

      state: {
        route: {
          query: {
            page: 1,
          },
        },
      },
    })
  })

  it('renders the entry', () => {
    const wrapper = shallowMount(List, {
      store,
      localVue,
      mocks: { $constants: { PAGE_SIZE: 10 } },
    })
    expect(wrapper.find('#list').exists()).toBe(true)
  })
})
