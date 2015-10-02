
var Entities = require('html-entities').AllHtmlEntities,
    entities  = new Entities();
function htmlParser(html) {
  var salta = false,
      text = "";
  for(var i= 0; i< html.length; i++) {
    if (html[i] === "<"){
      salta = true;
    }
    else if (html[i] === ">") {
      salta = false
    } else {
      if ( !salta ) {
        text += html[i];
      }
    }
  }
  return entities.decode(text);
}
function ReadTag(html,tag, htmlClass) {
  var subString, inicio, fin;
  /* Esta Función lee un html y busca la primera coinicdencia (tag y class) y regresa esa parte */
  inicio = html.indexOf("<" + tag + " " + 'class="' +htmlClass+'"');
  if (inicio > -1) {
    subString = html.substr(inicio);
    fin = subString.indexOf("</" + tag + ">");
    if (fin > -1) {
      subString = subString.substr(0, fin);
      return htmlParser(subString);
    }
  }
}

exports.ReadTag = ReadTag;