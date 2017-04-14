function displayQuestion(answer) {
  document.getElementById(answer + 'Question').style.display = "block";
  if (answer == "Neighbourhood") { // hide the div that is not selected
    document.getElementById('neighbourhood').style.display = "none";
  }
}
