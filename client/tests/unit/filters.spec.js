import {
  paramsToFilterConfiguration,
  filterConfigurationToParams,
  toggleFacetInConfiguration,
  MULTIPLE_VALUE_SEPARATOR,
} from '@/mixins/Filters'

describe('Filters.vue', () => {
  describe('toggleFacetInConfiguration', () => {
    it('toggles a value out of empty to empty', () => {
      const configuration = {
        year: [2019],
      }

      expect(toggleFacetInConfiguration(configuration, 'year', 2019)).toEqual(
        {},
      )
    })
    it('toggles a value into empty', () => {
      const configuration = {}

      expect(toggleFacetInConfiguration(configuration, 'year', 2019)).toEqual({
        year: [2019],
      })
    })
    it('toggles a value out of existing', () => {
      const configuration = {
        year: [2019, 2020, 2021],
        discipline: ['psychology'],
        journal: ['scientific-reports', 'european-neuropsychopharmacology'],
      }

      expect(toggleFacetInConfiguration(configuration, 'year', 2019)).toEqual({
        year: [2020, 2021],
        discipline: ['psychology'],
        journal: ['scientific-reports', 'european-neuropsychopharmacology'],
      })
    })
    it('toggles a value in', () => {
      const configuration = {
        year: [2019, 2021],
        discipline: ['psychology'],
        journal: ['scientific-reports', 'european-neuropsychopharmacology'],
      }

      expect(toggleFacetInConfiguration(configuration, 'year', 2020)).toEqual({
        year: [2019, 2021, 2020],
        discipline: ['psychology'],
        journal: ['scientific-reports', 'european-neuropsychopharmacology'],
      })
    })
  })
  describe('paramsToFilterConfiguration', () => {
    it('deserializes root path', () => {
      const params = {}
      const configuration = paramsToFilterConfiguration(params)
      expect(configuration).toEqual({})
    })

    it('deserializes all categories', () => {
      const params = {
        year: '2020',
        discipline: 'psychology',
        journal: 'scientific-reports',
        author: 'david-nutt',
      }

      const configuration = paramsToFilterConfiguration(params)

      expect(configuration).toEqual({
        year: [2020],
        discipline: ['psychology'],
        journal: ['scientific-reports'],
        author: ['david-nutt'],
      })
    })

    it('deserializes with multiple entries', () => {
      const params = {
        year: '2019/2020',
        discipline: 'psychology',
        journal: 'scientific-reports',
        author: 'david-nutt/felix-peppert',
      }

      const configuration = paramsToFilterConfiguration(params)

      expect(configuration).toEqual({
        year: [2019, 2020],
        discipline: ['psychology'],
        journal: ['scientific-reports'],
        author: ['david-nutt', 'felix-peppert'],
      })
    })
  })

  describe('filterConfigurationToParams', () => {
    it('serializes root path', () => {
      const configuration = {}
      const serialized = filterConfigurationToParams(configuration)
      expect(serialized).toEqual({})
    })

    it('serializes all categories', () => {
      const configuration = {
        year: [2020],
        discipline: ['psychology'],
        journal: ['scientific-reports'],
      }

      expect(filterConfigurationToParams(configuration)).toEqual({
        year: '2020',
        discipline: 'psychology',
        journal: 'scientific-reports',
      })
    })

    it('serializes with multiple entries', () => {
      const configuration = {
        year: [2019, 2020, 2021],
        discipline: ['psychology'],
        journal: ['scientific-reports', 'european-neuropsychopharmacology'],
      }
      expect(filterConfigurationToParams(configuration)).toEqual({
        year: '2019/2020/2021',
        discipline: 'psychology',
        journal: 'scientific-reports/european-neuropsychopharmacology',
      })
    })
  })
})
