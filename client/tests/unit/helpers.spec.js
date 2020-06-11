import { transformPublication } from '@/store/helpers'

describe('transformPublication', () => {
  it('add author names', () => {
    const publication = {
      authors: [
        {
          first_name: 'Testy',
          last_name: 'McTestface',
        },
        {
          first_name: 'Special',
          last_name: 'Sâusage',
        },
      ],
    }

    expect(publication.authorNames).toBeUndefined()

    const transformed = transformPublication(publication)
    expect(transformed.authorNames.length === 2)
    expect(transformed.authorNames[0]).toBe('Testy McTestface')
  })
})
