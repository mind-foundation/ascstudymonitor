class Datatable {
  getChevronToggleHTMLString(id) {
    const $div = $(
      `<div class='entry__chevron-wrapper'>&nbsp;</div>`
    )

    const html_chevron = `
      <svg xmlns="http://www.w3.org/2000/svg" class='toggles_datatable' data-id='${id}' width="35.912" height="20.077" viewBox="0 0 35.912 20.077" style="transform:rotate(-90deg);">
      <defs><style>.a{fill:none;stroke:#333;stroke-width:3px;}</style></defs>
      <path class="a" d="M36.107,2581,53,2597.9l-16.9,16.9" transform="translate(2615.851 -35.046) rotate(90)"/>
      </svg>
    `
    
    $div.append(html_chevron)
    return $div[0].outerHTML
  }

  toggle(id) {
    const isVisible = $(`div.entry[data-id="${id}"] .entry__abstract`).is(
      ':visible'
    )
    const $entry = $(`div.entry[data-id="${id}"]`);
    if (isVisible) {
        $entry
        .closest('tr')
        .find('.entry__chevron-wrapper svg')
        .css({
          transform: 'rotate(-90deg)',
        })

        $entry
        .find('h3')
        .css({cursor: 'pointer'})
    } else {
        $entry
        .closest('tr')
        .find('.entry__chevron-wrapper svg')
        .css({
          transform: 'rotate(0deg)',
        })

        $entry
        .find('h3')
        .css({cursor: 'text'})
    }

    $entry.find('.entry__downloads').fadeToggle(300)
    $entry.find('.entry__abstract').slideToggle(300)
  }

  open(id) {
    const isVisible = $(`div.entry[data-id="${id}"] .entry__abstract`).is(
      ':visible'
    )
    if (!isVisible) {
      App.Datatable.toggle(id)
    }
  } 

  updateColumnFilter(columnName, labels, patternBuilderFn) {
    /*
    Add a column filter given a column name and list of queries.
    patternBuilderFn is a callback [string] -> string that builds a regex to search the table.
    Use Datatable.draw() to render filtered data after all filters have been applied.
    */
    const column = this.dataTable.column(`${columnName}:name`)
    const queryRegex = patternBuilderFn(labels)
    console.log("[Datatable] set update filter", columnName, queryRegex);
    column.search(queryRegex, true, false);
  }

  draw() {
    this.dataTable.draw()
  }

  static renderAuthorForSearch(author) {
    return `${author.first_name} ${author.last_name}`
  }

  init() {
    const $table = $('.data-table')

    const dataTable = $table.DataTable({
      data: App.data,
      deferRender: true,
      columns: [
        {
          data: null,
          orderable: false,
          render: (data, type, row, meta) => {
            return this.getChevronToggleHTMLString(row.id)
          },
          width: '100px',
        },
        {
          data: 'content',
          render: (item, type, row) =>
            Handlebars.compile(
              document.getElementById('template-entry').innerHTML
            )(row),
        },

        // columns to filter by
        { name: 'year', data: 'year', defaultContent: '', visible: false },
        { name: 'disciplines', data: 'disciplines', render: disciplines => disciplines.join(" "), defaultContent: '', visible: false},
        { name: 'source', data: 'source', defaultContent: '', visible: false},
        { name: 'authors', data: 'authors', defaultContent: '', render: authors => authors.map(Datatable.renderAuthorForSearch).join(" "), visible: false},
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

    $('.title-bar__input').on('change keyup', function(event) {
      dataTable
        .search(
          String(event.target.value)
            .valueOf()
            .trim()
        )
        .draw()
    })

    $table.on('click',  function(event) {
      const target = event.target
      const nodeName = target.nodeName.toLowerCase()

      if (nodeName == 'div' || nodeName == 'svg' || nodeName == 'td' || nodeName == 'path') {
        const $target = $(target)
        const $chevron = $target.closest('div').find('svg')

        if ($chevron.hasClass('toggles_datatable')) {
          const id = $chevron.attr('data-id')
          console.log($chevron)
          App.Datatable.toggle(id)
        }
      }
    })

    setTimeout(() => {
      $('.data-table tfoot').remove()
    })

    this.dataTable = dataTable;
  }
}
window.App.Datatable = new Datatable()
