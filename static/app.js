window.App = {
  addFilter(column, label) {
    if (!App.filters) {
      App.filters = {}
    }

    if (!App.filters[column]) {
      App.filters[column] = []
    }

    App.filters[column].push(label)
  },

  removeFilter(column, label) {
    if (!App.filters) {
      return
    }

    if (!App.filters[column]) {
      return
    }

    App.filters[column] = App.filters[column].filter(item => item != label)
  },

  applyFilters() {
    // Filter by specific colu,n
  },

  search(newValue) {
    console.log('[Search] Update term: %s', newValue)
    window.scrollTo({ top: 0, left: 0, behavior: 'smooth' })

    // update value of input and simulate enter press
    const $el = $('.title-bar__input')
    $el.val(newValue)
    setTimeout(() => {
      $el.trigger('keyup')
    }, 0)
    return false
    // smooth scroll up
  },

  data: function() {
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
          // data.length = 10
          data = data.filter(d => d.file_attached)

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

    const data = await App.data()

    App.data = data

    //window.Menu.bootstrap(data)
    App.Datatable.init(data)

    setTimeout(() => window.__Mindblower__.stop(), 10)

    // const hasData = await this.data

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
    setTimeout(() => $(document).foundation(), 1000)
  },
}

$(document).ready(App.onDOMReady)
