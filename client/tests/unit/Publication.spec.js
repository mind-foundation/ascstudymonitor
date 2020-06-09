import { shallowMount, createLocalVue } from '@vue/test-utils'
import Vuex from 'vuex'
import Publication from '@/views/Publication.vue'

const localVue = createLocalVue()
localVue.use(Vuex)

describe('Publication.vue', () => {
  let store

  beforeEach(() => {
    store = new Vuex.Store({
      state: {
        route: {},
        publications: [
          {
            id: 'A',
            slug: '123456-A',
            websites: ['http://test.com'],
          },
        ],
      },
    })
  })

  it('matches snapshot', () => {
    const wrapper = shallowMount(Publication, { store, localVue })
    expect(wrapper.element).toMatchSnapshot()
  })

  it('renders the entry', () => {
    const wrapper = shallowMount(Publication, { store, localVue })
    expect(wrapper.find('.entry').exists()).toBe(true)
  })

  it('expands', async () => {
    const wrapper = shallowMount(Publication, {
      store,
      localVue,
      propsData: { publicationId: 'A' },
    })

    let downloads = wrapper.find('.entry__downloads-item')
    expect(downloads.element).toBeFalsy()

    wrapper.find('.chevron-wrapper').trigger('click')

    await wrapper.vm.$nextTick()

    downloads = wrapper.find('.entry__downloads-item')

    expect(downloads.isVisible()).toBe(true)
  })
})
