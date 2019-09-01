function filterPatternAny(labels) {
  if (labels.length == 0) {
    return ''
  }

  return '(' + labels.join('|') + ')'
}


window.App = {
  filters: {},
  
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

  fetch() {
    const MIND_ASC_STORAGE_KEY_CACHE = 'mind-asc-cache'
    const MIND_ASC_STORAGE_KEY_LAST = 'mind-asc-last'

    let lastCacheEntryDate = localStorage.getItem(MIND_ASC_STORAGE_KEY_LAST)
    let data = null
    const useCache = true // change me

    if (useCache && lastCacheEntryDate) {
      let cachedData = localStorage.getItem(MIND_ASC_STORAGE_KEY_CACHE)

      let msSinceLastAccess = -1
      const ONE_HOUR = 3600e3
      if (typeof cachedData === 'string') {
        let lastDate = new Date(lastCacheEntryDate)
        msSinceLastAccess = (+new Date() - lastDate) / 1000
        if (msSinceLastAccess <= ONE_HOUR) {
          data = JSON.parse(cachedData)
          
          // for faster development
          // data.length = 100
          // data = data.filter(d => d.file_attached)

          console.info(
            '[Cache] Hit: Loading %s entries from %ss ago',
            data.length,
            Math.round(msSinceLastAccess / 1000)
          )
        }
      }
    }

    if (!data) {
      data = $.getJSON('/documents.json')
    }

    return data
  },

  async onDOMReady() {
    window.__Mindblower__.start()

    const data = await App.fetch()

    App.data = data

    //window.Menu.bootstrap(data)
    setTimeout(() => {
      App.Datatable.init(data)

      const getDistinct = key =>
        Array.from(new Set(data.flatMap(d => d[key])))
          .filter(Boolean)
          .sort()

      App.Menu = {
        open: [],
      }

      App.distinct = ['disciplines', 'source', 'authors', 'year'].reduce(
        (bag, key) => ({
          ...bag,
          [key]: getDistinct(key),
        }),
        {}
      )

      initMenu()
      $(document).foundation()
      window.__Mindblower__.stop()
    })
    // const hasData = await this.data
  },
}

$(document).ready(App.onDOMReady)
