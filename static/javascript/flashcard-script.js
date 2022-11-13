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

// /**
//  * Updates the thumbnail on a drop zone element.
//  *
//  * @param {HTMLElement} dropZoneElement
//  * @param {File} file
//  */
// function updateThumbnail(dropZoneElement, file) {
//   let thumbnailElement = dropZoneElement.querySelector(".drop-zone__thumb");

//   // First time - remove the prompt
//   if (dropZoneElement.querySelector(".drop-zone__prompt")) {
//     dropZoneElement.querySelector(".drop-zone__prompt").remove();
//   }

//   // First time - there is no thumbnail element, so lets create it
//   if (!thumbnailElement) {
//     thumbnailElement = document.createElement("div");
//     thumbnailElement.classList.add("drop-zone__thumb");
//     dropZoneElement.appendChild(thumbnailElement);
//   }

//   thumbnailElement.dataset.label = file.name;

//   // Show thumbnail for image files
//   if (file.type.startsWith("image/")) {
//     const reader = new FileReader();

//     reader.readAsDataURL(file);
//     reader.onload = () => {
//       thumbnailElement.style.backgroundImage = `url('${reader.result}')`;
//     };
//   } else {
//     thumbnailElement.style.backgroundImage = null;
//   }
// }


// THIS ONE IS FOR CREATING Inputs

function getQuestion(){

  var question = window.getSelection();
  const para = document.createElement("input");
  para.setAttribute('value', question); 
  para.setAttribute('name', 'question');
  para.setAttribute('id', 'question');
  highlightQuestion(question.toString());
  const element = document.getElementById("form1");
  element.appendChild(para);

  return 0;
}

function highlightQuestion(text) {
  var inputText = document.getElementById("inputText");
  var innerHTML = inputText.innerHTML;
  var index = innerHTML.indexOf(text);
  if (index >= 0) { 
   innerHTML = innerHTML.substring(0,index) + "<span style=\"background-color: green\">" + text + "</span>" + innerHTML.substring(index + text.length);
   inputText.innerHTML = innerHTML;
  }
}

function getAnswer(){
  var answer = window.getSelection();
  const para = document.createElement("input");
  para.setAttribute('value', answer); 
  para.setAttribute('name', 'answer');
  para.setAttribute('id', 'answer');
  highlightAnswer(answer.toString());
  const element = document.getElementById("form1");
  element.appendChild(para);
  return 0;
}

function highlightAnswer(text) {
  var inputText = document.getElementById("inputText");
  var innerHTML = inputText.innerHTML;
  var index = innerHTML.indexOf(text);
  if (index >= 0) { 
   innerHTML = innerHTML.substring(0,index) + "<span style=\"background-color: red\">" + text + "</span>" + innerHTML.substring(index + text.length);
   inputText.innerHTML = innerHTML;
  }
}