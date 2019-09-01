function initMenu() {
  new Vue({
    el: '#menu-content',
    data: {
      distinct: App.distinct,
      keys: App,
      open: App.Menu.open,
      filters: App.filters,
      items: {
        disciplines: {
          expanded: false,
          title: 'Disciplines',
          total: App.distinct.disciplines.length,
          data: App.distinct.disciplines.map(discipline => ({
            active: false,
            label: discipline,
            count: App.data.filter(
              d => d.disciplines && d.disciplines.includes(discipline)
            ).length,
          })),
        },
        source: {
          expanded: false,
          title: 'Journals',
          total: App.distinct.source.length,
          data: App.distinct.source.map(source => ({
            active: false,
            label: source,
            count: App.data.filter(d => d.source === source).length,
          })),
        },
        authors: {
          expanded: false,
          title: 'Authors',
          total: App.distinct.authors.length,
          data: App.distinct.authors.map(author => ({
            active: false,
            label: author,
            count: App.data.filter(d => d.authors && d.authors.includes(author))
              .length,
          })),
        },
        year: {
          expanded: false,
          title: 'Years',
          total: App.distinct.year.length,
          data: App.distinct.year.map(year => ({
            active: false,
            label: year,
            count: App.data.filter(d => d.year === year).length,
          })),
        },
      },
      data: App.data,
    },
    computed: {
      filterClassObject: function() {
        console.log('this', this)
        console.log('label', this.filters)
        console.log('key', this.key)
        return {
          active:
            this.filters[this.key] && this.filters[this.key].includes(d.label),
        }
      },
    },
    methods: {
      handleMenuCategoryToggle(event) {
        console.log('menu category toggle')
        const $target = $(event.target)

        const $li = $target.closest('li')
        const key = $li.data('key')
        toggle(App.Menu.open, key)
        const $ul = $li.find('ul')
        console.log('query', $ul)
        $ul.stop().slideToggle(300)
      },
      filterItemClick() {
        const $target = $(event.target)

        const key = $target.closest('li[data-key]').data('key')
        console.log('key', key)
        const value = $target.closest('li[data-value]').data('value')
        console.log('value', value)
        console.log('call toggle filer', key, value)
        App.toggleFilter(key, value)
      },
      formatLabel(label) {
        return typeof label !== 'object'
          ? label
          : `${label.first_name} ${label.last_name}`
      },
    },
  })

  // var data = dataWithoutNormalizedAuthors.map(d => ({
  //       ...d,
  //       authors: d.authors
  //         ? d.authors.map(a => [a.last_name, a.first_name].join(', '))
  //         : null,
  //     }))
}

function toggle(collection, item) {
  var idx = collection.indexOf(item)
  if (idx !== -1) {
    collection.splice(idx, 1)
  } else {
    collection.push(item)
  }
}
