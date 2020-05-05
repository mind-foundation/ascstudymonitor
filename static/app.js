function filterPatternAny(labels) {
  if (labels.length == 0) {
    return ''
  }

  return '(' + labels.join('|') + ')'
}

function getDistinct(data, key) {
  // get distinct values for key from data
  return Array.from(new Set(data.flatMap(d => d[key]))).filter(Boolean)
}

window.App = {
  filters: {},
  Menu: { open: [] },
  data: null,
  distinct: null,

  initDistinct() {
    App.distinct = ['disciplines', 'source', 'authorLabels', 'year'].reduce(
      (bag, key) => ({
        ...bag,
        [key]: getDistinct(App.data, key),
      }),
      {}
    )
  },

  toggleFilter(column, label) {
    label = label.toString()

    if (!App.filters[column]) {
      App.filters[column] = []
    }

    if (App.filters[column].includes(label)) {
      App.filters[column] = App.filters[column].filter(item => item != label)
    } else {
      App.filters[column].push(label)
    }

    App.applyFilters()
    App.Menu.$forceUpdate()
  },

  applyFilters() {
    // Apply filter state by specific columns
    Object.entries(App.filters).forEach(([column, labels]) => {
      App.Datatable.updateColumnFilter(column, labels, filterPatternAny)
    })

    App.Datatable.draw()
  },

  async onDOMReady() {
    window.__Mindblower__.start()

    Sentry.init({
      dsn: 'https://a35eb03c2845422ca06eae7625922e9a@sentry.io/1553227',
    })

    const documents = new Documents()
    documents.get().then(data => {
      App.data = data
      App.Datatable.init(data)
      App.initDistinct(data)
      initMenu()
      $(document).foundation()
      window.__Mindblower__.stop()
    })
  },
}

$(document).ready(App.onDOMReady)
