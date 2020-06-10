export function transformPublication(p) {
  p.authorNames = p.authors.map(a =>
    [a.first_name, a.last_name].filter(Boolean).join(' '),
  )
  return p
}
