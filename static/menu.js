function initMenu() {
  App.Menu = new Vue({
    el: '#menu-content',
    data: {
      distinct: App.distinct,
      keys: App,
      open: App.Menu.open,
      filters: App.filters,
      items: {
        disciplines: {
          title: 'Disciplines',
          total: App.distinct.disciplines.length,
          data: App.distinct.disciplines
            .map(discipline => ({
              label: discipline,
              count: App.data.filter(
                d => d.disciplines && d.disciplines.includes(discipline)
              ).length,
            }))
            .sort((a, b) => b.count - a.count),
        },
        source: {
          title: 'Journals',
          total: App.distinct.source.length,
          data: App.distinct.source
            .map(source => ({
              label: source,
              count: App.data.filter(d => d.source === source).length,
            }))
            .sort((a, b) => b.count - a.count),
        },
        authors: {
          title: 'Authors',
          total: App.distinct.authorLabels.length,
          data: App.distinct.authorLabels
            .map(author => ({
              label: author,
              count: App.data.filter(
                d => d.authorLabels && d.authorLabels.includes(author)
              ).length,
            }))
            .sort((a, b) => b.count - a.count),
        },
        year: {
          title: 'Years',
          total: App.distinct.year.length,
          data: App.distinct.year
            .sort((a, b) => b - a)
            .map(year => ({
              label: year.toString(),
              count: App.data.filter(d => d.year === year).length,
            })),
        },
      },
      data: App.data,
    },
    methods: {
      handleMenuCategoryToggle(event) {
        const $target = $(event.target)

        const $li = $target.closest('li')
        const key = $li.data('key')
        toggle(App.Menu.open, key)
        const $ul = $li.find('ul')
        $ul.stop().slideToggle(300)
      },
      filterItemClick() {
        const $target = $(event.target)

        const key = $target.closest('li[data-key]').data('key')
        const value = $target.closest('li[data-value]').data('value')
        App.toggleFilter(key, value)
      },
    },
  })
}

function toggle(collection, item) {
  var idx = collection.indexOf(item)
  if (idx !== -1) {
    collection.splice(idx, 1)
  } else {
    collection.push(item)
  }
}
