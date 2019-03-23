function startEffect() {
  const width = $(".datatable-spinner__wrapper").width()
  const height = $(".datatable-spinner__wrapper").height()
  let circles = ""
  const total = 50 // number of overlapping circles
  const size = 900 // diameter of circles (px)

  const top = index =>
    -(size / 2) + (size / 2) * Math.cos((2 * Math.PI * (index - 1)) / total)

  const left = index =>
    -(size / 2) + (size / 2) * Math.sin((2 * Math.PI * (index - 1)) / total)

  for (
    let i = 1, end = total, asc = 1 <= end;
    asc ? i <= end : i >= end;
    asc ? i++ : i--
  ) {
    circles += `<div class=\"datatable-spinner__circle index-${i}\" style=\" \
      width:${size}px; \
      height:${size}px; \
      top:${top(i)}px; \
      left:${left(i)}px; \
    \"></div>`
  }

  //    + height / 2
  //  + width / 2

  $(".datatable-spinner__wrapper").html(circles)
}
