import { shallowMount, createLocalVue } from '@vue/test-utils'
import Vuex from 'vuex'
import Navigation from '@/components/Navigation.vue'
import constants from '../../src/constants'

const localVue = createLocalVue()
localVue.prototype.$constants = constants
localVue.use(Vuex)

describe('Navigation.vue', () => {
  let store

  beforeEach(() => {
    store = new Vuex.Store({
      state: {
        route: {},
        loaded: false,
      },
    })
  })

  it('matches snapshot', () => {
    const wrapper = shallowMount(Navigation, { store, localVue })
    expect(wrapper.element).toMatchSnapshot()
  })

  it('renders the entry', () => {
    const wrapper = shallowMount(Navigation, { store, localVue })
    expect(wrapper.find('#menu').exists()).toBe(true)
  })
})
