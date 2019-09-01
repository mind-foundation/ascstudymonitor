window.Menu = {
  render() {
    console.log("[Menu] render")
    
    const $menu = $('#menu-content')

    if (!Menu.template) {
      Menu.template = Handlebars.compile(
        document.getElementById('template-menu').innerHTML
      )
    }

    Menu.sortItems()
    const items = Object.entries(Menu.items).map(([key, item]) => ({...item, key}))

    $menu.html(Menu.template({ items }))
  },

  filterItemClick(column, label, currentActive) {
    if (currentActive) {
      console.log("[Menu] deactivate", column, label)
      Menu.toggleActive(column, label, false)
      App.removeFilter(column, label)
    }
    else {
      console.log("[Menu] activate", column, label)
      Menu.toggleActive(column, label, true)
      App.addFilter(column, label)
    }
  },

  toggleActive(column, label, active) {
    Menu.items[column] = Menu.items[column].data.map(entry => {
      if (entry.label == label) {
        entry.active = active
      }
      return entry
    })

    Menu.render()
  },

  toggleExpanded(column, expanded) {
    console.log("[Menu] expand", column, expanded)
    Menu.items[column].expanded = expanded
    Menu.render()
  },

  sortItems() {
    Object.values(Menu.items).map(item => {
      return item.data.sort((a, b) => {
        if (a.active == b.active) {
          return b.count - a.count
        } else {
          return b.active ? 1 : -1
        }})
    })
  },

  handleMenuCategoryToggle(key) {
    const $a = $(`.menu__category-link[data-key="${key}"]`)
    console.log($a)
    
    var isActive = Menu.items[key].expanded
    Menu.toggleExpanded(key, !isActive)

    $a.data('active', !isActive)
    $a.find('svg').css({
      transform: `rotate(${isActive ? 90 : 0}deg)`,
    })
  },

  bootstrap(dataWithoutNormalizedAuthors) {
    var data = dataWithoutNormalizedAuthors.map(d => ({
      ...d,
      authors: d.authors
        ? d.authors.map(a => [a.last_name, a.first_name].join(', '))
        : null,
    }))

    const getDistinct = key =>
      Array.from(new Set(data.flatMap(d => d[key])))
        .filter(Boolean)
        .sort()

    var [allDisciplines, allSources, allAuthors, allYears] = [
      'disciplines',
      'source',
      'authors',
      'year',
    ].map(getDistinct)

    Menu.items = {
      'discipline': {
        expanded: false,
        title: 'Disciplines',
        total: allDisciplines.length,
        data: allDisciplines
          .map(discipline => ({
            active: false,
            label: discipline,
            count: data.filter(
              d => d.disciplines && d.disciplines.includes(discipline)
            ).length,
          })),
      },
      'source': {
        expanded: false,
        title: 'Journals',
        total: allSources.length,
        data: allSources
          .map(source => ({
            active: false,
            label: source,
            count: data.filter(d => d.source === source).length,
          })),
      },
      'author': {
        expanded: false,
        title: 'Authors',
        total: allAuthors.length,
        data: allAuthors
          .map(author => ({
            active: false,
            label: author,
            count: data.filter(d => d.authors && d.authors.includes(author))
              .length,
          })),
      },
      'year': {
        expanded: false,
        title: 'Years',
        total: allYears.length,
        data: allYears
          .map(year => ({
            active: false,
            label: year,
            count: data.filter(d => d.year === year).length,
          })),
      },
    }

    // console.log("items", items)
    Menu.render()
  },
}
