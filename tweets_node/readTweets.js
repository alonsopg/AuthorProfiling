var fs = require('fs');
var htmlParser = require('./htmlParser'),
    https = require('https'),
    tweets = [],
    path = process.argv[2],
    dir = process.argv[3];

var urls = JSON.parse(fs.readFileSync(path,{encoding:'utf8'}));
function httpSync(url, body, numberDocuments) {
  https.get(url, function readTweet(res,body) {
    res.setEncoding('utf8');
    res.on('data', function getRes(chunck) {
      body += chunck;
    });
    res.on('end', function endRes() {
      tweets.push({"index" : url.substr(url.lastIndexOf('/')+1), "data" :htmlParser.ReadTag(body, "p", "js-tweet-text tweet-text")});
      if (tweets.length === urls.length) {
        procesarTweets();
      }
    });
        
  });
}
urls.forEach(function (url) {
  httpSync(url.url,"");
})

function procesarTweets() {
  var jsonPath  = path.substr(path.lastIndexOf('/')+1);
  fs.writeFile( dir + jsonPath, JSON.stringify(tweets), function (err) {
    if (err) {
      console.log(err);
    } else {
      console.log("Archivo " + jsonPath + " escrito.");
    }
  })
}