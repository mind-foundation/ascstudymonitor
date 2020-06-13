import VueSocialSharing from 'vue-social-sharing'
import { shallowMount, createLocalVue } from '@vue/test-utils'
import SocialBar from '@/components/SocialBar.vue'

const localVue = createLocalVue()

localVue.use(VueSocialSharing)

describe('SocialBar.vue', () => {
  const publication = {
    slug: '6666666666-hi-im-a-slug',
    title: 'read me i’m interesting',
  }

  it('matches snapshot', () => {
    const wrapper = shallowMount(SocialBar, {
      localVue,
      propsData: { publication },
    })
    expect(wrapper).toMatchSnapshot()
  })

  it('renders the container', () => {
    const wrapper = shallowMount(SocialBar, {
      localVue,
      propsData: { publication },
    })
    expect(wrapper.find('#social-bar').exists()).toBe(true)
  })
})
