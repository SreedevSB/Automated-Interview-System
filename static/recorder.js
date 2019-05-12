


var buttonRecord = document.getElementById("record");
var buttonStop = document.getElementById("stop");

buttonStop.disabled = true;

buttonRecord.onclick = function() {
    startQn()
};

buttonStop.onclick = function() {
    endQn()
};



function startQn(){
    
    // var url = window.location.href + "record_status";
    buttonRecord.disabled = true;
    buttonStop.disabled = false;
    
    // disable download link
    var downloadLink = document.getElementById("download");
    downloadLink.text = "";
    downloadLink.href = "";

    // XMLHttpRequest
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4 && xhr.status == 200) {
            // alert(xhr.responseText);
        }
    }
    xhr.open("POST", "/record_status");
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhr.send(JSON.stringify({ status: "true" , candidate:"Sam"}));
}

function endQn(){
    buttonRecord.disabled = false;
    buttonStop.disabled = true;    

    // XMLHttpRequest
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4 && xhr.status == 200) {
            // alert(xhr.responseText);

            // enable download link
            var downloadLink = document.getElementById("download");
            downloadLink.text = "Download Video";
            downloadLink.href = "/static/video.avi";
        }
    }
    xhr.open("POST", "/record_status");
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhr.send(JSON.stringify({ status: "false", candidate:"Sam"}));
}


questions=[
    "Tell me something ",
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec elementum massa in neque rutrum, fringilla venenatis ipsum euismod. Nunc bibendum imperdiet lectus scelerisque tincidunt",
    "3.Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec elementum massa in neque rutrum, fringilla venenatis ipsum euismod. Nunc bibendum imperdiet lectus scelerisque tincidunt"
]

