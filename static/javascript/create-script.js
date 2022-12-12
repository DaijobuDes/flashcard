function loadFile(url, callback) {
    PizZipUtils.getBinaryContent(url, callback);
}
const terms = [];
const definitions = [];
const def_pos = [];
const term_btn = document.getElementById("term");
const def_btn = document.getElementById("definition");
const submit = document.getElementById('submit');

submit.disabled = true;
def_btn.disabled = true;

 function str2xml(str) {
    if (str.charCodeAt(0) === 65279) {
       // BOM sequence
       str = str.substr(1);
    }
    return new DOMParser().parseFromString(str, "text/xml");
 }

 function getParagraphs(content) {
    const zip = new PizZip(content);
    const xml = str2xml(zip.files["word/document.xml"].asText());
    const paragraphsXml = xml.getElementsByTagName("w:p");
    const paragraphs = [];

    for (let i = 0, len = paragraphsXml.length; i < len; i++) {
       let fullText = "";
       const textsXml =
             paragraphsXml[i].getElementsByTagName("w:t");
       for (let j = 0, len2 = textsXml.length; j < len2; j++) {
             const textXml = textsXml[j];
             if (textXml.childNodes) {
                fullText += textXml.childNodes[0].nodeValue;
             }
       }

       paragraphs.push(fullText);
    }
    return paragraphs;
 }

 function gettext() {
   const selectedFile = document.getElementById('myFile').files[0];
   loadFile(
      URL.createObjectURL(selectedFile),
      function (error, content) {
         if (error) {
            throw error;
         }
         const cont = document.getElementById("inputText");
         var text = getParagraphs(content);
         cont.innerHTML = '';
         for(i = 0; i < text.length; i++){
         if(text[i].length === 0)
            continue;
         cont.append(text[i]);
         cont.append(document.createElement('br'));
         }
         customSelect(element, onSelect);
      }
   );
 }

var alreadySelected = [];
 function customSelect(target, onSelect) {
   var oldHTML = target.innerHTML;
   
   // this is the regex that wraps the words with spans:
   target.innerHTML = oldHTML.replace(/[\d\w\<\>'\’\-\!\?\;\:\"\|\=\+\~\@\#\$\%\^\&\*\(\)\“\[]+[\s,.”~\]\n]*/g, '<span>$&</span>'); // \<>'’-!()
   var spans = target.querySelectorAll('span');
   
   // I used a basic blue/white style, but you can change it in the CSS
   // using the ".text-selected" selector 
   alreadySelected = [];
   var setSpanOn = function(span) {
     alreadySelected.push(span);
    //  span.className = 'text-selected';
    span.classList.add("text-selected");
   };

   var setSpanOff = function(span) {
    try {
      span.classList.remove("text-selected");
    }
    catch(err) {
      console.log(err.message);
    }
   };
   // here starts the logic
   var isSelecting = false;
   for (var i=0, l=spans.length; i<l; i++) {
     (function span_handlers(span, pos) {
     
       // when the user starts holding the mouse button
       span.onmousedown = function() {
         // deselect previous selection, if any:
         alreadySelected.splice(0).forEach(setSpanOff);
         
         // and enable selection:
         isSelecting = true;
         span.onmouseenter();
       };
       
       // the main logic, we check if we need to set or not this span as selected:
       span.onmouseenter = function() {
         if (!isSelecting)
           return;
         
         // if already selected
         var j = alreadySelected.indexOf(span);
         if (j >= 0) {
           // then deselect the spans that were selected after this span
           alreadySelected.splice(j+1).forEach(setSpanOff);
         }
         else {
           // else if is not the first, check if the user selected another word 
           // one line down or up. This is done by checking the indexes:
           if (alreadySelected.length) {
             var last = alreadySelected[alreadySelected.length-1];
             var posLast = [].indexOf.call(spans, last);
             var typeSibling = pos > posLast ? 'nextSibling' : 'previousSibling';
             while (1) {
               last = last[typeSibling];
               if (last !== span)
                 setSpanOn(last);
               else break;
             }
           }
           setSpanOn(span);
         }
       };
       
       // when the user hold up the mouse button:
       span.onmouseup = function() {
         isSelecting = false;
         
         //  call the onSelect function passing the selected spans content:
         if (typeof onSelect === 'function') {
           var spansSelected = target.querySelectorAll('.text-selected');
           var text = [].map.call(spansSelected, function(span) {
             return span.textContent || '';
           }).join('').trim();
           onSelect(text);
         }
       };
     })(spans[i], i);
   }
 };
 
 // Usage:
 var element = document.getElementById('inputText');
 var temp = "";
 var onSelect = function(text) {
   temp = text;
 };

 function getQuestion(){
   var selected =  document.getElementsByClassName("text-selected");
   const log = (element) => element === temp;

   if(selected.length === 0) 
      return;

   if(terms.find(log)){
      alert("this term is already in database");
      return;
   }
   term_btn.disabled = true;
   def_btn.disabled = false;
   submit.disabled = true;

   var len = selected.length - 1;
   if(selected.length > 1)
   for(i = 0; i < selected.length; i++){
      switch(i){
         case 0: 
         selected[i].classList.add('qn', 'selected-st');
         break;
         case len:
         selected[i].classList.add('qn', 'selected-end');
         break;
         default:
         selected[i].classList.add('qn');
      }
   }
   else
      selected[0].classList.add('qn', 'selected-st', 'selected-end');
   spans = [];
   terms.push(temp);
   return;
}

function getAnswer(){
   var selected =  document.getElementsByClassName("text-selected");
   if(selected.length === 0) 
      return;
   term_btn.disabled = false;
   def_btn.disabled = true;
   submit.disabled = false;
   var len = selected.length - 1;
   if(selected.length > 1)
   for(i = 0; i < selected.length; i++){
      selected[i].setAttribute("name", def_pos.length);
      switch(i){
         case 0: 
         selected[i].classList.add('def', 'selected-st');
         break;
         case len:
         selected[i].classList.add('def', 'selected-end');
         break;
         default:
         selected[i].classList.add('def');
      }
   }
   else{
      selected[0].setAttribute("name", def_pos.length);
      selected[0].classList.add('def', 'selected-st', 'selected-end');
   }
   spans = [];
   definitions.push(temp);
   var items = document.getElementsByName(def_pos.length);
   def_pos.push(items);
   return;
}

function eraseQuestion(){
   if(term_btn.disabled === true){
      alert("please finish term and definition tuple before erasure");
      return;
   }

   if(temp === ""){
      alert("empty string");
      return;
   }

   const log = (element) => element === temp;
   const ind = terms.findIndex(log);
   if(ind === -1){
      alert("this is not yet a term");
      return;
   }
   for(i = 0; i < alreadySelected.length; i++)
      alreadySelected[i].className = "";
   if(ind > -1){
      terms[ind] = "";
      definitions[ind] = "";
      for(i = 0; i < def_pos[ind].length; i++)
         def_pos[ind][i].className = "";
   }
   return;
}

function questionSubmit(){
   const form1 = document.getElementById('form1');
   for(i = 0; i < terms.length; i++){
      if(terms[i].length === 0) continue;
      const input = document.createElement("input");
      input.setAttribute("name", "question");
      input.setAttribute("value", terms[i]);
      const input2 = document.createElement("input");
      input2.setAttribute("name", "answer");
      input2.setAttribute("value", definitions[i]);
      form1.append(input);
      form1.append(input2);
   }
   return;
}

customSelect(element, onSelect);