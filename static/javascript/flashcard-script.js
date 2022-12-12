document.querySelectorAll(".drop-zone__input").forEach((inputElement) => {
  const dropZoneElement = inputElement.closest(".drop-zone");

  dropZoneElement.addEventListener("click", (e) => {
    inputElement.click();
  });

  inputElement.addEventListener("change", (e) => {
    if (inputElement.files.length) {
      updateThumbnail(dropZoneElement, inputElement.files[0]);
    }
  });

  dropZoneElement.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropZoneElement.classList.add("drop-zone--over");
  });

  ["dragleave", "dragend"].forEach((type) => {
    dropZoneElement.addEventListener(type, (e) => {
      dropZoneElement.classList.remove("drop-zone--over");
    });
  });

  dropZoneElement.addEventListener("drop", (e) => {
    e.preventDefault();

    if (e.dataTransfer.files.length) {
      inputElement.files = e.dataTransfer.files;
      updateThumbnail(dropZoneElement, e.dataTransfer.files[0]);
    }

    dropZoneElement.classList.remove("drop-zone--over");
  });
});

// THIS ONE IS FOR CREATING Inputs

var loadItem = function(event) {
  document.querySelector(".drop-zone__prompt").remove();
  document.getElementById("thumb").style.display = "inline";
  var output = document.getElementById('output');

  output.src = "docx.png";

  output.onload = function() {
     URL.revokeObjectURL(output.src) // free memory
  }
}

// function loadFile(url, callback) {
//   PizZipUtils.getBinaryContent(url, callback);
// }
// function gettext() {

//   const selectedFile = document.getElementById('myFile').files[0];
//   loadFile(
//         URL.createObjectURL(selectedFile),
//         function (error, content) {
//            if (error) {
//               throw error;
//            }
//            var content = document.getElementById("inputText");
//            var zip = new PizZip(content);
//            var doc = new window.docxtemplater(zip);
//            var text = doc.getFullText();
//            console.log(text);
//         }
//   );
// }