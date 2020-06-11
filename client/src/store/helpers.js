export function transformPublication(p) {
  p.authorNames = p.authors.map(a =>
    [a.first_name, a.last_name].filter(Boolean).join(' '),
  )
  if (!p.disciplines) {
    p.disciplines = []
  }
  if (!p.year) {
    console.error('[Data] Publication %s / %s is missing year', p.id, p.title)
  }
  return p
}
