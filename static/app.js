window.App = {}

const MIND_ASC_STORAGE_KEY_CACHE = 'mind-asc-cache'
const MIND_ASC_STORAGE_KEY_LAST = 'mind-asc-last'

var $table

function updateSearchValue(newValue) {
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
}

// function spinnerDOMStringFactory(label) {}

$(document).ready(function() {
  $table = $('.data-table')

  let data = localStorage.getItem(MIND_ASC_STORAGE_KEY_CACHE)
  window.__Mindblower__.start()

  const useCache = true /* edit me */
  let msSinceLastAcccess = -1
  if (useCache && data) {
    const ONE_HOUR = 3600e3
    let last = localStorage.getItem(MIND_ASC_STORAGE_KEY_LAST)
    if (last) {
      let lastDate = new Date(last)
      msSinceLastAcccess = (+new Date() - lastDate) / 1000
      if (msSinceLastAcccess > ONE_HOUR) {
        console.info('[Cache] Expired! %s seconds old', msSinceLastAcccess)
        localStorage.removeItem(MIND_ASC_STORAGE_KEY_LAST)
        localStorage.removeItem(MIND_ASC_STORAGE_KEY_CACHE)
        return fetchNew()
      }
    }

    data = JSON.parse(data)
    data.length = 10

    console.info(
      '[Cache] Hit: Loading %s entries from %ss ago',
      data.length,
      Math.round(msSinceLastAcccess / 1000)
    )
    App.Datatable.init($table, data)
  } else {
    console.info('[Cache] None found.')
    window.__Mindblower__.start()
    fetchNew()
  }
})

function fetchNew() {
  console.info('[Cache] Refreshing..')
  $.getJSON('/documents.json', function(data) {
    console.info('[Cache] Refreshing.. Done!')
    localStorage.setItem(MIND_ASC_STORAGE_KEY_CACHE, JSON.stringify(data))
    localStorage.setItem(MIND_ASC_STORAGE_KEY_LAST, new Date().toISOString())

    App.Datatable.init($table, data)
  })
}
