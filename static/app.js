function renderAuthors(data, type, row) {
  if (data && data.length) {
    return data
      .map(function(author) {
        const first_name = author.first_name ? author.first_name : "";
        const last_name = author.last_name ? author.last_name : "";
        return [first_name, last_name].join(" ");
      })
      .join("<br >");
  } else {
    return "";
  }
}

function renderDisciplines(data, type, row) {
  if (data && data.length) {
    return data.join("<br >");
  } else {
    return "";
  }
}

function renderAbstract(abstract) {
  /* Convert newlines to paragraphs */
  return abstract
    .split("\n")
    .map(function(par) {
      return "<p>" + par + "</p>";
    })
    .join("\n");
}

function transformIdentifiers(data, type, row) {
  return data ? Object.values(data).join(" ") : "";
}

function transformKeywords(data, type, row) {
  return data ? data.join(" ") : "";
}

function furtherInfo(doc) {
  const abstract = doc.abstract
    ? `
                <h2 class="furtherInfoHeader">Abstract</h2>
                <div class="furtherInfoText">${renderAbstract(
                  doc.abstract
                )}</div>
            `
    : "";
  const citation = doc.citation
    ? `
                <h2 class="furtherInfoHeader">Citation</h2>
                <div class="furtherInfoText">${doc.citation}</div>
            `
    : "";

  const website = doc.websites
    ? `<a target="_blank" rel="noopener noreferrer" href="${
        doc.websites[0]
      }">Show on Publisher Website</a>`
    : "";
  const download = doc.file_attached
    ? `<a target="_blank" rel="noopener noreferrer" href="/download/${
        doc.id
      }">Download full text</a>`
    : "<span>Fulltext available from Publisher</span>";

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
            `;
}

function spinnerDOMStringFactory(label) {
  return `<div class="datatable-spiner__container">
  <div class="datatable-spiner__circle">
  
  </div><p>${label}</p></div>`
}
$(document).ready(function() {
  console.log("DOM ready")
  const table = $("#ascTable").DataTable({
    ajax: {
      url: "/documents.json",
      dataSrc: ""
    },
    columns: [
      {
        data: null,
        orderable: false,
        width: "10px",
        defaultContent: '<i data-feather="arrow-down"></i>'
      },
      { data: "title", width: "auto" },
      { data: "authors", render: renderAuthors, width: "20%" },
      {
        data: "year",
        defaultContent: "",
        width: "5%",
        className: "dt-center"
      },
      {
        data: "disciplines",
        defaultContent: "",
        render: renderDisciplines,
        width: "10%"
      },
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
    processing: true,
    language: {
      paginate: {
        first: "<<",
        last: ">>",
        next: ">",
        previous: "<"
      },
      loadingRecords: spinnerDOMStringFactory('Loading..'),
      processing: spinnerDOMStringFactory('Processing..'),
    },
    drawCallback: feather.replace,
    autoWidth: false
  });

  $("#ascTable tBody").on("click", "tr", function() {
    const tr = $(this).closest("tr");

    if (tr.hasClass("furtherInfoRow")) {
      // clicked on child
      return;
    }

    const row = table.row(tr);
    const handle = table.cell(row, 0).node();
    const title = table.cell(row, 1);

    const evenOdd = row.node().classList.contains("even") ? "even" : "odd";

    if (row.child.isShown()) {
      row.child.hide();
      tr.removeClass("shown");
      handle.innerHTML = '<i data-feather="arrow-down"></i>';
    } else {
      row.child(furtherInfo(row.data()), `${evenOdd} furtherInfoRow`);
      row.child.show();
      tr.addClass("shown");
      handle.innerHTML = '<i data-feather="arrow-up"></i>';
    }

    feather.replace();
  });

  $("#ascSearch").on("change keyup", function(event) {
    const query = $("#ascSearch").val();
    table.search(query).draw();
  });
});
