function allowDrop(event) {
  event.preventDefault();
  event.target.style.border = "4px dotted purple";
}

function drop(event) {
  event.preventDefault();
  var files = event.dataTransfer.files;
      var filesName=files[0].name;
      var extStart=filesName.lastIndexOf(".");
      var ext=filesName.substring(extStart,filesName.length).toUpperCase();
      if(ext!=".JPG"&&ext!=".PNG"&&ext!=".XML"){ //判断是否是需要的问件类型
        alert("请选择.jpg、.png、.xml类型的文件上传！");
        return false;
      }else{
        var formData = new FormData();
        formData.append('file', event.dataTransfer.files[0]);
        uploadFile(formData);
      }
}

function uploadFile(formData) {
    var xhr = new XMLHttpRequest();
    xhr.open('POST', 'http://0.0.0.0:5000/upload', false);
    xhr.send(formData);
}