var fs = require("fs"),
    url, tweets, dir = process.argv[2],dirToCheck = process.argv[3], tweets_descargados= 0, tweets_supuestos = 0;

fs.readdir(dir, function(err, list){
  
  list.forEach(function(file) {
    tweets_descargados += JSON.parse(fs.readFileSync(dir + file, {encoding:'utf8'})).length;
    console.log(JSON.parse(fs.readFileSync(dir + file, {encoding:'utf8'})).length,JSON.parse(fs.readFileSync(dirToCheck +file, {encoding:'utf8'})).length, file);
  });
  console.log(list.length);
  console.log("Tweets descargados: ", tweets_descargados);
});