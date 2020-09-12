import { shallowMount, createLocalVue } from '@vue/test-utils'
import Vuex from 'vuex'
import PublicationListItem from '../PublicationListItem.vue'

const localVue = createLocalVue()
localVue.use(Vuex)

describe('PublicationListItem.vue', () => {
  let store
  let propsData

  beforeEach(() => {
    propsData = {
      slug: '123456-A',
    }
    store = new Vuex.Store({
      state: {
        route: {},
      },
      modules: {
        publications: {
          namespaced: true,
          state: {
            items: [
              {
                id: 'A',
                slug: '123456-A',
                websites: ['http://test.com'],
                title: 'Title',
                recommendations: [{ id: 'R1' }],
              },
            ],
          },
        },
        recommendations: {
          namespaced: true,
          state: {
            items: [
              {
                id: 'R1',
                title: 'Title',
              },
            ],
          },
        },
      },
    })
  })

  it('renders the entry', () => {
    const wrapper = shallowMount(PublicationListItem, {
      store,
      localVue,
      propsData,
    })
    expect(wrapper.find('.row').exists()).toBe(true)
  })

  it('expands', async () => {
    const wrapper = shallowMount(PublicationListItem, {
      store,
      localVue,
      propsData,
    })

    let downloads = wrapper.find('.entry__downloads-item')
    expect(downloads.element).toBeFalsy()

    wrapper.find('.chevron-wrapper').trigger('click')

    await wrapper.vm.$nextTick()

    downloads = wrapper.find('.entry__downloads-item')

    expect(downloads.isVisible()).toBe(true)
  })
})
