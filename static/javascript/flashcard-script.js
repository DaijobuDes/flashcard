var loadItem = function(event) {
  document.querySelector(".drop-zone__prompt").remove();
  document.getElementById("thumb").style.display = "inline";
  var output = document.getElementById('output');

  output.src = "docx.png";

  output.onload = function() {
     URL.revokeObjectURL(output.src) // free memory
  }
}

function shareLink(){
  navigator.clipboard.writeText(window.location.href);
  alert("Link has been copied. You can share to other people now!");
  return;
}