import { shallowMount, createLocalVue } from '@vue/test-utils'
import Vuex from 'vuex'
import Navigation from '../Navigation.vue'
import constants from '@/constants'

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

  it('renders the entry', () => {
    const wrapper = shallowMount(Navigation, { store, localVue })
    expect(wrapper.find('#menu').exists()).toBe(true)
  })
})
