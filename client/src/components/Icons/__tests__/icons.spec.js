import { shallowMount } from '@vue/test-utils'
import Close from '../Close'
import Abstract from '../Abstract'
import Chevron from '../Chevron'
import Author from '../Author'
import Download from '../Download'
import Filters from '../Filters'
import Link from '../Link'
import PublicationChevron from '../PublicationChevron'
import Science from '../Science'

describe('Icons', () => {
  let store
  ;[
    [Close, 'Close'],
    [Abstract, 'Abstract'],
    [Chevron, 'Chevron'],
    [Author, 'Author'],
    [Download, 'Download'],
    [Filters, 'Filters'],
    [Link, 'Link'],
    [PublicationChevron, 'PublicationChevron'],
    [Science, 'Science'],
  ].forEach(([Component, name]) => {
    it(name, () => {
      const wrapper = shallowMount(Component, { store })
      expect(wrapper.find('svg').isVisible()).toBe(true)
    })
  })

  it('Abstract', () => {
    const wrapper = shallowMount(Abstract, { store })
    expect(wrapper.find('svg').isVisible()).toBe(true)
  })

  it('Author', () => {
    const wrapper = shallowMount(Author, { store })
    expect(wrapper.find('svg').isVisible()).toBe(true)
  })

  it('Chevron', () => {
    const wrapper = shallowMount(Chevron, { store })
    expect(wrapper.find('svg').isVisible()).toBe(true)
  })

  it('Download', () => {
    const wrapper = shallowMount(Download, { store })
    expect(wrapper.find('svg').isVisible()).toBe(true)
  })
  it('Download', () => {
    const wrapper = shallowMount(Download, { store })
    expect(wrapper.find('svg').isVisible()).toBe(true)
  })
})
