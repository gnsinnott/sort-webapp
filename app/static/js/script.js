var coll = document.getElementsByClassName("collapsible");
var i;

for (i = 0; i < coll.length; i++) {
  coll[i].addEventListener("click", function() {
    this.classList.toggle("active");
    var content = this.nextElementSibling;
    if (content.style.display === "block") {
      content.style.display = "none";
    } else {
      content.style.display = "block";
    }
  });
}


function delete_record() {
    var urlArray = window.location.pathname.split('/');
    var data = {'id' : urlArray[urlArray.length -1] };
    var response = confirm("Are you sure you want to delete this record?")
    if (response=true) {
        var xhr = new XMLHttpRequest();
        xhr.open('POST', "/api/v1/delete_record", true);
        xhr.setRequestHeader("Content-Type", "application/json; charset=UTF-8");
        xhr.onreadystatechange = function () {
            if (xhr.readyState === 4 && xhr.status === 200) {
                var res = JSON.parse(xhr.response);
                console.log(res);
                if (res.status == "true") {
                    document.getElementById("status").innerHTML = "Record has been deleted.";
                }
                else {
                    document.getElementById("status").innerHTML = "Record could not be deleted.";
                }
            }
        };
        xhr.send(JSON.stringify(data));
        return false;
    }
}

function restore_record() {
  var urlArray = window.location.pathname.split('/');
  var data = {'id' : urlArray[urlArray.length -1] };
  var response = confirm("Are you sure you want to restore this record?")
  if (response=true) {
      var xhr = new XMLHttpRequest();
      xhr.open('POST', "/api/v1/restore_record", true);
      xhr.setRequestHeader("Content-Type", "application/json; charset=UTF-8");
      xhr.onreadystatechange = function () {
          if (xhr.readyState === 4 && xhr.status === 200) {
              var res = JSON.parse(xhr.response);
              console.log(res);
              if (res.status == "true") {
                  document.getElementById("status").innerHTML = "Record has been restored.";
              }
              else {
                  document.getElementById("status").innerHTML = "Record could not be restored.";
              }
          }
      };
      xhr.send(JSON.stringify(data));
      return false;
  }
}