// Generated by CoffeeScript 1.3.3
var postUpload;

window.upload = function(event) {
  var doc, document, _i, _len, _ref;
  document = [];
  _ref = event.files;
  for (_i = 0, _len = _ref.length; _i < _len; _i++) {
    doc = _ref[_i];
    document.append({
      "title": doc.data.filename,
      "FPUrl": doc.url
    });
  }
  return $.post("localhost:5000/addDocument", {
    documents: document
  }, postUpload(), "json");
};

postUpload = function() {
  return null;
};
