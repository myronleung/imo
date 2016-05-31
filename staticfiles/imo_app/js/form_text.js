function removeText() {
  var text = document.getElementsByClassName("input-field").textContent;
  text.remove()
}

var eltext = document.getElementsByClassName("input-field");
elText.onclick = removeText;
