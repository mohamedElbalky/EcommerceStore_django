
function fillField (id) {
    document.getElementById(id).style.height = "35px"

}

window.onscroll = () => {
  let value = screenY
  console.log(value)
}

function goUp() {
    scroll({
      top: 0,
      behavior: "smooth"
    })
  }