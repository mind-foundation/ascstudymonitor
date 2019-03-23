function templateFactory(templateKey) {
  return function(item, type, row) {
    var template = Handlebars.compile(
      document.getElementById("template-title-column").innerHTML
    )
    return template({ row })
  }
}

Handlebars.registerHelper("disciplines", function disciplinesHelper(
  items,
  options
) {
  if (!items) return ""
  var out = "<ul>"

  for (var i = 0, l = items.length; i < l; i++) {
    out =
      out +
      "<li><a href='#" +
      options.fn(items[i]) +
      "' onClick=\"updateSearchValue('" +
      items[i] +
      "')\">" +
      options.fn(items[i]) +
      "</a></li>"
  }

  return out + "</ul>"
})

Handlebars.registerHelper("authors", function(items, options) {
  if (!items) return ""
  var out = "<ul>"

  // console.log(items)
  for (var i = 0, l = items.length; i < l; i++) {
    out = out + "<li>" + authorToText(items[i]) + "</li>"
  }

  return out + "</ul>"
})

Handlebars.registerHelper("sanitize", function(object) {
  // console.log("santiize: ", object)
  const firstName = object.row.authors.first_name
  const lastName = object.row.authors.last_name

  return new Handlebars.SafeString(firstName + " " + lastName)
})
