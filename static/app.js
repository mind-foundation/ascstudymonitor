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

  data: async function() {
    console.log('fetching data')
    const MIND_ASC_STORAGE_KEY_CACHE = 'mind-asc-cache'
    const MIND_ASC_STORAGE_KEY_LAST = 'mind-asc-last'

    let lastCacheEntryDate = localStorage.getItem(MIND_ASC_STORAGE_KEY_LAST)
    let data = null
    const useCache = true // change me

    if (useCache && lastCacheEntryDate) {
      let cachedData = localStorage.getItem(MIND_ASC_STORAGE_KEY_CACHE)

      let msSinceLastAcccess = -1
      const ONE_HOUR = 3600e3
      if (typeof cachedData === 'string') {
        let lastDate = new Date(lastCacheEntryDate)
        msSinceLastAcccess = (+new Date() - lastDate) / 1000
        if (msSinceLastAcccess <= ONE_HOUR) {
          data = JSON.parse(cachedData)
          data.length = 10

          console.info(
            '[Cache] Hit: Loading %s entries from %ss ago',
            data.length,
            Math.round(msSinceLastAcccess / 1000)
          )
        }
      }
    }

    if (!data) {
      data = await $.getJSON('/documents.json')
    }

    return data
  },

  async onDOMReady() {
    window.__Mindblower__.start()

    const data = await App.data()

    App.Datatable.init(data)
    setTimeout(() => window.__Mindblower__.stop(), 10)

    // const hasData = await this.data
  },
}

$(document).ready(App.onDOMReady)
