function bootstrapMenu(data) {
  console.log("bootstrapping menu")
  var template = Handlebars.compile(
    document.getElementById("template-menu").innerHTML
  )

  var allDisciplines = Array.from(
    new Set(data.flatMap(d => d.disciplines))
  ).sort()

  var allSources = Array.from(new Set(data.map(d => d.source))).sort()

  // var allAuthors = Array.from(new Set(data.flatMap(d => d.authors))).sort()
  // return console.log(allAuthors)

  var items = [
    {
      key: "disciplines",
      title: "Disciplines",
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
      data: allSources
        .map(source => ({
          label: source,
          count: data.filter(d => d.source === source).length
        }))
        .sort((a, b) => b.count - a.count)
    }
    // {
    //   key: "authors",
    //   title: "Authors",
    //   data: allAuthors.map(author => ({
    //     label: author,
    //     count: data.filter(d => d.authors && d.authors.includes(author)).length
    //   }))
    // }
  ]
  console.log("items", items)
  console.log(template({ items }))
  $("#menu-content").html(template({ items }))
  $(document).foundation()
}
