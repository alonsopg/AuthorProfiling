var fs = require('fs'),
    xml2js = require('xml2js'),
    parser = new xml2js.Parser(),
    urls = [], truth;
//Funciones


function leerArchivo( data) {
  parser.parseString(data, function parsingData(err,result) {
    if (err) {
      return err;
    }
    for(var i = 0; i < result.author.documents[0].document.length;i++ ) {
      urls.push({"url" : result.author.documents[0].document[i].$.url});
    }
    
            
  });
       
}

function readFiles(path,list) {
  for (var i = 0; i< list.length;i++) {
    data = fs.readFileSync(path + list[i]+".xml", {encoding : 'utf8'});
    leerArchivo(data);
    fs.writeFileSync(process.argv[3]+list[i]+'.json',JSON.stringify(urls));
    urls = [];
    
   
  }
}

function xmlReader (path) {
  //list = fs.readdirSync(path);
  var files = [];
  list = fs.readFileSync(path + 'truth.txt', {encoding : 'utf8'});
  truth = list.split("\n");
  truth.pop();
  for ( var i= 0; i < truth.length; i++) {
    files.push(truth[i].substr(0,32));
  }
  readFiles(path, files);
  console.log(urls.length);
  
}
xmlReader(process.argv[2]);
