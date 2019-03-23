MIND_ASC_STORAGE_KEY_CACHE = "mind-asc-cache"
MIND_ASC_STORAGE_KEY_LAST = "mind-asc-last"

function updateSearchValue(newValue) {
  console.log("[Search] Update term: %s", newValue)
  window.scrollTo({ top: 0, left: 0, behavior: "smooth" })

  // update value of input and simulate enter press
  const $el = $(".search-bar__input")
  $el.val(newValue)
  setTimeout(() => {
    $el.trigger("keyup")
  }, 0)
  return false
  // smooth scroll up
}

function renderAbstract(abstract) {
  /* Convert newlines to paragraphs */
  return abstract
    .split("\n")
    .map(function(par) {
      return "<p>" + par + "</p>"
    })
    .join("\n")
}

function transformIdentifiers(data, type, row) {
  return data ? Object.values(data).join(" ") : ""
}

function transformKeywords(data, type, row) {
  return data ? data.join(" ") : ""
}

function furtherInfo(doc) {
  const abstract = doc.abstract
    ? `
                <h2 class="furtherInfoHeader">Abstract</h2>
                <div class="furtherInfoText">${renderAbstract(
                  doc.abstract
                )}</div>
            `
    : ""
  const citation = doc.citation
    ? `
                <h2 class="furtherInfoHeader">Citation</h2>
                <div class="furtherInfoText">${doc.citation}</div>
            `
    : ""

  const website = doc.websites
    ? `<a target="_blank" rel="noopener noreferrer" href="${
        doc.websites[0]
      }">Show on Publisher Website</a>`
    : ""
  const download = doc.file_attached
    ? `<a target="_blank" rel="noopener noreferrer" href="/download/${
        doc.id
      }">Download full text</a>`
    : "<span>Fulltext available from Publisher</span>"

  return `
                <div class="furtherInfo">
                    <div class="furtherInfoContent">
                        ${abstract}
                        ${citation}
                    </div>
                    <div class="furtherInfoAction">
                        ${website}
                        ${download}
                    </div>
                </div>
            `
}

function spinnerDOMStringFactory(label) {}

$(document).ready(function() {
  let data = localStorage.getItem(MIND_ASC_STORAGE_KEY_CACHE)

  setTimeout(startEffect, 0)

  const useCache = true /* edit me */
  let secondsSinceLastAccess = -1
  if (useCache && data) {
    let last = localStorage.getItem(MIND_ASC_STORAGE_KEY_LAST)
    if (last) {
      let lastDate = new Date(last)
      secondsSinceLastAccess = (+new Date() - lastDate) / 1000
      if (secondsSinceLastAccess > 60) {
        console.info("[Cache] Expired! %s seconds old", secondsSinceLastAccess)
        localStorage.removeItem(MIND_ASC_STORAGE_KEY_LAST)
        localStorage.removeItem(MIND_ASC_STORAGE_KEY_CACHE)
        return fetchNew()
      }
    }

    data = JSON.parse(data)
    console.info(
      "[Cache] Hit: Loading %s entries from %ss ago",
      data.length,
      Math.round(secondsSinceLastAccess)
    )
    initDataTable(data)
  } else {
    console.info("[Cache] None found.")
    fetchNew()
  }
})

function fetchNew() {
  console.info("[Cache] Refreshing..")
  $.getJSON("/documents.json", function(data) {
    console.info("[Cache] Refreshing.. Done!")
    localStorage.setItem(MIND_ASC_STORAGE_KEY_CACHE, JSON.stringify(data))
    localStorage.setItem(MIND_ASC_STORAGE_KEY_LAST, new Date().toISOString())

    initDataTable(data)
  })
}

function initDataTable(data) {
  const table = $(".data-table").DataTable({
    data,
    columns: [
      {
        data: null,
        orderable: false,
        width: "10px",
        defaultContent: '<i data-feather="arrow-down"></i>'
      },
      {
        data: "title",
        render: templateFactory("template-title-column"),
        width: "50%"
      },
      { data: "authors", defaultContent: "", visible: false },

      { data: "source", defaultContent: "", width: "20%" },

      // column to define order
      { data: "created", visible: false, searchable: false },

      // hidden but searchable columns
      { data: "abstract", defaultContent: "", visible: false },
      {
        data: "keywords",
        defaultContent: "",
        render: transformKeywords,
        visible: false
      },
      {
        data: "identifiers",
        defaultContent: "",
        render: transformIdentifiers,
        visible: false
      },
      { data: "year", defaultContent: "", visible: false }
    ],
    pageLength: 20,
    dom: "t p i",
    ordering: true,
    order: [[6, "desc"], [1, "asc"]],
    orderClasses: false,
    language: {
      paginate: {
        first: "<<",
        last: ">>",
        next: ">",
        previous: "<"
      }
    },
    drawCallback: feather.replace,
    autoWidth: false
  })

  $(".data-table tBody").on("click", "tr", function() {
    const tr = $(this).closest("tr")

    if (tr.hasClass("furtherInfoRow")) {
      // clicked on child
      return
    }

    const row = table.row(tr)
    const handle = table.cell(row, 0).node()
    const title = table.cell(row, 1)

    console.log(row)

    const evenOdd = row.node().classList.contains("even") ? "even" : "odd"

    if (row.child.isShown()) {
      row.child.hide()
      tr.removeClass("shown")
      handle.innerHTML = '<i data-feather="arrow-down"></i>'
    } else {
      row.child(furtherInfo(row.data()), `${evenOdd} furtherInfoRow`)
      row.child.show()
      tr.addClass("shown")
      handle.innerHTML = '<i data-feather="arrow-up"></i>'
    }

    feather.replace()
  })

  $(".search-bar__input").on("change keyup", function(event) {
    table
      .search(
        String(event.target.value)
          .valueOf()
          .trim()
      )
      .draw()
  })

  setTimeout(() => {
    $(".data-table tfoot").remove()
  })
}

function authorToText(author) {
  return `${author.first_name} ${author.last_name}`
}
