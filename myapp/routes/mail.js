var express = require('express');
var router = express.Router();

formidable = require('formidable')
util = require('util')
fs = require('fs-extra')
/* GET home page. *//*
router.get('/', function (req, res){
  res.writeHead(200, {'Content-Type': 'text/html' });
  var form = '<form action="/akshay/upload" enctype="multipart/form-data" method="post"><input multiple="multiple" name="upload" type="file" /><br><br><input type="submit" value="Upload" /></form>';
  res.end(form); 
}); 
*/
router.post('/upload', function (req, res){

  var form = new formidable.IncomingForm();
    console.log(req.param("eid"))
  //console.log(req.method)
  form.parse(req, function(err, fields, files) {
    console.log(req.param("eid"))
    console.log(util.inspect({files: files}));
    res.render('home', { title: 'Started working',data :'You will receive an email when done'});    
  });

  form.on('end', function(fields, files) {
    /* Temporary location of our uploaded file */
    var temp_path1 = this.openedFiles[0].path;
    var temp_path2 = this.openedFiles[1].path;
    /* The file name of the uploaded file */
    var file_name1 = this.openedFiles[0].name;
    var file_name2 = this.openedFiles[1].name;
    /* Location where we want to copy the uploaded file */
    var new_location = 'uploads/';

    fs.copy(temp_path1, new_location + file_name1, function(err) {  
      if (err) {
        console.error(err);
      } else {
    fs.copy(temp_path2, new_location + file_name2,function(err){
      if (err) {
        console.error(err);
      } else {
                var python_shell = require('python-shell')
                var options = {'scriptPath' : __dirname,'args' : [new_location+file_name1,new_location+file_name2]}
                console.log("Calling python script!")
                python_shell.run('../../test.py',options,function(err,results){
                if(err)
                  throw err;
                console.log(results[0]+"Send Mail now!")
                })
                console.log("Script is now running!")
              }
    });
  }});
});
});

module.exports = router;
