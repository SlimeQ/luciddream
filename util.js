var fs   = require('fs');
var path = require('path');

exports.hrsToSec = function(hr) {
  return hr * 60 * 60;
}
exports.timestamp = function() {
  return Math.round(+new Date()/1000);
}
exports.ensureExists = function(path, mask, cb) {
  if (typeof mask == 'function') {
    // allow the `mask` parameter to be optional
    cb = mask;
    mask = 0777;
  }
  fs.mkdir(path, mask, function(err) {
    if (err) {
      // ignore the error if the folder already exists
      if (err.code == 'EEXIST') {
        cb(null);
      } else {
        // something else went wrong
        cb(err);
      }
    } else {
      // successfully created folder
      cb(null);
    }
  });
}

// function to encode file data to base64 encoded string
exports.base64_encode = function(file) {
    // read binary data
    var bitmap = fs.readFileSync(file);
    // convert binary data to base64 encoded string
    return new Buffer(bitmap).toString('base64');
}

// function to create file from base64 encoded string
exports.base64_decode = function(base64str, file) {
    // create buffer object from base64 encoded string, it is important to tell the constructor that the string is base64 encoded
    // console.log(base64str);
    var bitmap = new Buffer(base64str.replace(/^data:image\/(png|gif|jpeg);base64,/,''), 'base64');
    // write buffer to file
    fs.writeFileSync(file, bitmap);
    console.log('******** File created from base64 encoded string ********');
}
