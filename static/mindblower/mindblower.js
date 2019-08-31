class Mindblower {
  constructor() {}
  start() {
    console.log("Start effect")
    const width = $("#mindblower").width()
    const height = $("#mindblower").height()
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
      circles += `<div class=\"mindblower__circle index-${i}\" style=\" \
      width:${size}px; \
      height:${size}px; \
      top:${top(i)}px; \
      left:${left(i)}px; \
    \"></div>`
    }

    //    + height / 2
    //  + width / 2

    $("#mindblower__effect-container").html(circles)
  }

  stop() {
    $("#mindblower").remove()
  }
}

window.__Mindblower__ = new Mindblower()
