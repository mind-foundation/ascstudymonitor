function bootstrapMenu(dataWithoutNormalizedAuthors) {
  var data = dataWithoutNormalizedAuthors.map(d => ({
    ...d,
    authors: d.authors
      ? d.authors.map(a => [a.last_name, a.first_name].join(", "))
      : null
  }))

  console.log("bootstrapping menu")
  var template = Handlebars.compile(
    document.getElementById("template-menu").innerHTML
  )

  const getDistinct = key =>
    Array.from(new Set(data.flatMap(d => d[key])))
      .filter(Boolean)
      .sort()

  var [allDisciplines, allSources, allAuthors, allYears] = [
    "disciplines",
    "source",
    "authors",
    "year"
  ].map(getDistinct)

  var items = [
    {
      key: "discipline",
      title: "Disciplines",
      total: allDisciplines.length,
      data: allDisciplines
        .map(discipline => ({
          label: discipline,
          count: data.filter(
            d => d.disciplines && d.disciplines.includes(discipline)
          ).length
        }))
        .sort((a, b) => b.count - a.count)
    },
    {
      key: "source",
      title: "Journals",
      total: allSources.length,
      data: allSources
        .map(source => ({
          label: source,
          count: data.filter(d => d.source === source).length
        }))
        .sort((a, b) => b.count - a.count)
    },
    {
      key: "author",
      title: "Authors",
      total: allAuthors.length,
      data: allAuthors
        .map(author => ({
          label: author,
          count: data.filter(d => d.authors && d.authors.includes(author))
            .length
        }))
        .sort((a, b) => b.count - a.count)
    },
    {
      key: "year",
      title: "Years",
      total: allYears.length,
      data: allYears
        .map(year => ({
          label: year,
          count: data.filter(d => d.year === year).length
        }))
        .sort((a, b) => b.label - a.label)
    }
  ]
  console.log("items", items)
  // console.log(template({ items }))
  $("#menu-content").html(template({ items }))
  $(document).foundation()
}
