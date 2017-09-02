var express = require('express');
var router = express.Router();

formidable = require('formidable')
util = require('util')
fs = require('fs-extra')
/* GET home page. */
router.get('/', function (req, res){
  res.writeHead(200, {'Content-Type': 'text/html' });
  var form = '<form action="/akshay/upload" enctype="multipart/form-data" method="post"><input multiple="multiple" name="upload" type="file" /><br><br><input type="submit" value="Upload" /></form>';
  res.end(form); 
}); 

router.post('/upload', function (req, res){
  var form = new formidable.IncomingForm();
  console.log(req.params)
  form.parse(req, function(err, fields, files) {
    console.log(util.inspect({files: files}));
    res.render('index', { title: 'Started working',data :'You will receive an email when done'});    
  });

  form.on('end', function(fields, files) {
    /* Temporary location of our uploaded file */
    var temp_path = this.openedFiles[0].path;
    /* The file name of the uploaded file */
    var file_name = this.openedFiles[0].name;
    /* Location where we want to copy the uploaded file */
    var new_location = 'uploads/';

    fs.copy(temp_path, new_location + file_name, function(err) {  
      if (err) {
        console.error(err);
      } else {
        var python_shell = require('python-shell')
  var options = {
    'scriptPath' : __dirname,
    'args' : ['1','2']
  }
  console.log("Calling python script!")
  python_shell.run('../../test.py',options,function(err,results){
      if(err)
        throw err;
      console.log(results[0]+"Send Mail now!")
      })
        console.log("Script is now running!")
      }
    });
  });
});

module.exports = router;
