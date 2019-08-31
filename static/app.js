const MIND_ASC_STORAGE_KEY_CACHE = 'mind-asc-cache'
const MIND_ASC_STORAGE_KEY_LAST = 'mind-asc-last'

const HTML_CHEVRON_DOWN =
  '<svg xmlns="http://www.w3.org/2000/svg" width="35.912" height="20.077" viewBox="0 0 35.912 20.077"><defs><style>.a{fill:none;stroke:#333;stroke-width:3px;}</style></defs><path class="a" d="M36.107,2581,53,2597.9l-16.9,16.9" transform="translate(2615.851 -35.046) rotate(90)"/></svg>'
const HTML_CHEVRON_RIGHT =
  '<svg xmlns="http://www.w3.org/2000/svg" width="35.912" height="20.077" viewBox="0 0 35.912 20.077" style="transform:rotate(270deg);"><defs><style>.a{fill:none;stroke:#333;stroke-width:3px;}</style></defs><path class="a" d="M36.107,2581,53,2597.9l-16.9,16.9" transform="translate(2615.851 -35.046) rotate(90)"/></svg>'

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

function renderAbstract(abstract) {
  /* Convert newlines to paragraphs */
  return abstract
    .split('\n')
    .map(function(par) {
      return '<p>' + par + '</p>'
    })
    .join('\n')
}

function transformIdentifiers(data, type, row) {
  return data ? Object.values(data).join(' ') : ''
}

function transformKeywords(data, type, row) {
  return data ? data.join(' ') : ''
}

function furtherInfo(doc) {
  const abstract = doc.abstract
    ? `
                <div class="furtherInfoText">${renderAbstract(
                  doc.abstract
                )}</div>
            `
    : ''

  const website = doc.websites
    ? `<a target="_blank" rel="noopener noreferrer" href="${
        doc.websites[0]
      }">Show on Publisher Website</a>`
    : ''
  const download = doc.file_attached
    ? `<a target="_blank" rel="noopener noreferrer" href="/download/${doc.id}">Download full text</a>`
    : '<span>Fulltext available from Publisher</span>'

  return `
                <div class="furtherInfo">
                    <div class="furtherInfoContent">
                        ${abstract}
                    </div>
                    <div class="furtherInfoAction">
                        ${website}
                        ${download}
                    </div>
                </div>
            `
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
    initDataTable(data)
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

    initDataTable(data)
  })
}

function initDataTable(data) {
  setTimeout(window.__Mindblower__.stop, 0)
  window.data = data
  bootstrapMenu(data)
  const dataTable = $table.DataTable({
    data,
    deferRender: true,
    columns: [
      {
        data: null,
        orderable: false,
        defaultContent: HTML_CHEVRON_DOWN,
        width: '100px',
      },
      {
        data: 'content',
        render: (item, type, row) =>
          Handlebars.compile(
            document.getElementById('template-entry').innerHTML
          )(row),
      },
      { data: 'year', defaultContent: '', visible: false },
    ],
    pageLength: 20,
    dom: 't p i',
    ordering: true,
    order: [[2, 'desc']],
    orderClasses: false,
    language: {
      paginate: {
        first: '<<',
        last: '>>',
        next: '>',
        previous: '<',
      },
    },

    autoWidth: false,
  })

  $('.data-table tBody').on('click', 'tr', function() {
    const tr = $(this).closest('tr')

    if (tr.hasClass('furtherInfoRow')) {
      // clicked on child
      return
    }

    const row = dataTable.row(tr)
    const handle = dataTable.cell(row, 0).node()
    const title = dataTable.cell(row, 1)

    const evenOdd = row.node().classList.contains('even') ? 'even' : 'odd'

    if (row.child.isShown()) {
      row.child.hide()
      tr.removeClass('shown')
      handle.innerHTML = HTML_CHEVRON_DOWN
    } else {
      row.child(furtherInfo(row.data()), `${evenOdd} furtherInfoRow`)
      row.child.show()
      tr.addClass('shown')
      handle.innerHTML = HTML_CHEVRON_RIGHT
    }
  })

  $('.title-bar__input').on('change keyup', function(event) {
    dataTable
      .search(
        String(event.target.value)
          .valueOf()
          .trim()
      )
      .draw()
  })

  setTimeout(() => {
    $('.data-table tfoot').remove()
  })
}

function authorToText(author) {
  return `${author.first_name} ${author.last_name}`
}

// var DataTablesLinkify = function(dataTable) {
//     this.dataTable = dataTable;
//     this.url = location.protocol+'//'+location.host+location.pathname;
//     this.link = function() {
//         return this.url +
//             '?dtsearch='+this.dataTable.search() +
//             '&dtpage='+this.dataTable.page();
//             //more params like current sorting column could be added here
//     }
//     //based on http://stackoverflow.com/a/901144/1407478
//     this.getParam = function(name) {
//         name = name.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]");
//         var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"),
//             results = regex.exec(location.search);
//         return results === null ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));
//     }
//     this.restore = function() {
//         var page = this.getParam('dtpage'),
//             search = this.getParam('dtsearch');
//         if (search) this.dataTable.search(search).draw(false);
//         if (page) this.dataTable.page(parseInt(page)).draw(false);
//         //more params to take care of could be added here
//     }
//     this.restore();
//     return this;
// };

// function syncURLWithtable() {
//   linkify = DataTablesLinkify(table)
// }
