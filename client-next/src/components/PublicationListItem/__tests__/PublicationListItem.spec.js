import { shallowMount } from '@vue/test-utils'
import PublicationListItem from '../PublicationListItem.vue'

describe('PublicationListItem.vue', () => {
  let propsData

  beforeEach(() => {
    propsData = {
      slug: '123456-A',
      publication: {
        abstract:
          'Psychedelic drugs, such as psilocybin and LSD, represent unique tools for researchers investigating the neural origins of consciousness. Currently, the most compelling theories of how psychedelics exert their effects is by increasing the complexity of brain activity and moving the system towards a critical point between order and disorder, creating more dynamic and complex patterns of neural activity. While the concept of criticality is of central importance to this theory, few of the published studies on psychedelics investigate it directly, testing instead related measures such as algorithmic complexity or Shannon entropy. We propose using the fractal dimension of functional activity in the brain as a measure of complexity since findings from physics suggest that as a system organizes towards criticality, it tends to take on a fractal structure. We tested two different measures of fractal dimension, one spatial and one temporal, using fMRI data from volunteers under the influence of both LSD and psilocybin. The first was the fractal dimension of cortical functional connectivity networks and the second was the fractal dimension of BOLD time-series. We were able to show that both psychedelic drugs significantly increased the fractal dimension of functional connectivity networks, and that LSD significantly increased the fractal dimension of BOLD signals, with psilocybin showing a non-significant trend in the same direction. With both LSD and psilocybin, we were able to localize changes in the fractal dimension of BOLD signals to brain areas assigned to the dorsal-attentional network. These results show that psychedelic drugs increase the fractal character of activity in the brain and we see this as an indicator that the changes in consciousness triggered by psychedelics are associated with evolution towards a critical zone.',
        authors: [
          {
            firstName: 'Thomas F.',
            lastName: 'Varley',
          },
          {
            firstName: 'Robin L.',
            lastName: 'Carhart-Harris',
          },
          {
            firstName: 'Leor',
            lastName: 'Roseman',
          },
          {
            firstName: 'David K.',
            lastName: 'Menon',
          },
          {
            firstName: 'Emmanuel A.',
            lastName: 'Stamatakis',
          },
        ],
        created: '2020-09-21 17:01:18.222000',
        disciplines: [
          {
            value: 'Neuropharmacology',
          },
        ],
        fileAttached: false,
        id: 'bb02d375-ec00-36ad-8eeb-87e84bb20269',
        keywords: [
          {
            value: 'Complexity',
          },
          {
            value: 'Consciousness',
          },
          {
            value: 'Criticality',
          },
          {
            value: 'Entropy',
          },
          {
            value: 'Fractal',
          },
          {
            value: 'LSD',
          },
          {
            value: 'Networks',
          },
          {
            value: 'Psilocybin',
          },
          {
            value: 'Psychedelic',
          },
          {
            value: 'fMRI',
          },
        ],
        slug:
          'serotonergic-psychedelics-lsd-psilocybin-increase-the-of-in-bb02d375',
        journal: {
          value: 'PLoS ONE',
        },
        title:
          'Serotonergic Psychedelics LSD & Psilocybin Increase the Fractal Dimension of Cortical Brain Activity in Spatial and Temporal Domains',
        websites: [
          'https://www.sciencedirect.com/science/article/pii/S1053811920305358?via%3Dihub',
          'http://dx.doi.org/10.1101/517847',
        ],
        year: {
          value: 2019,
        },
      },
    }
  })

  it('renders the entry', () => {
    const wrapper = shallowMount(PublicationListItem, {
      propsData,
    })
    expect(wrapper.find('.chevron-wrapper').exists()).toBe(true)
  })

  it('expands', async () => {
    const wrapper = shallowMount(PublicationListItem, {
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
