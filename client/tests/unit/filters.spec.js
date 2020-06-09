import {
  deserializeFilterConfiguration,
  serializeFilterConfiguration,
  toggleFacetInConfiguration,
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
  describe('deserializeFilterConfiguration', () => {
    it('deserializes root path', () => {
      const pathname = '/'
      const serialized = deserializeFilterConfiguration(pathname)
      expect(serialized).toEqual({})
    })

    it('deserializes all categories', () => {
      const pathname =
        '/year:2020/discipline:psychology/journal:scientific-reports'
      const serialized = deserializeFilterConfiguration(pathname)
      expect(serialized).toEqual({
        year: [2020],
        discipline: ['psychology'],
        journal: ['scientific-reports'],
      })
    })

    it('deserializes with multiple entries', () => {
      const pathname =
        '/year:2019,2020,2021/discipline:psychology/journal:scientific-reports,european-neuropsychopharmacology'
      const serialized = deserializeFilterConfiguration(pathname)
      expect(serialized).toEqual({
        year: [2019, 2020, 2021],
        discipline: ['psychology'],
        journal: ['scientific-reports', 'european-neuropsychopharmacology'],
      })
    })
  })

  describe('serializeFilterConfiguration', () => {
    it('serializes root path', () => {
      const configuration = {}
      const serialized = serializeFilterConfiguration(configuration)
      expect(serialized).toEqual('/')
    })

    it('serializes all categories', () => {
      const configuration = {
        year: [2020],
        discipline: ['psychology'],
        journal: ['scientific-reports'],
      }

      expect(serializeFilterConfiguration(configuration)).toEqual(
        '/year:2020/discipline:psychology/journal:scientific-reports',
      )
    })

    it('serializes with multiple entries', () => {
      const configuration = {
        year: [2019, 2020, 2021],
        discipline: ['psychology'],
        journal: ['scientific-reports', 'european-neuropsychopharmacology'],
      }
      expect(serializeFilterConfiguration(configuration)).toEqual(
        '/year:2019,2020,2021/discipline:psychology/journal:scientific-reports,european-neuropsychopharmacology',
      )
    })
  })
})
