


var buttonRecord = document.getElementById("record");
var buttonStop = document.getElementById("stop");

buttonStop.disabled = true;

buttonRecord.onclick = function() {
    process(0)
};

buttonStop.onclick = function() {
    endQn()
};



function startQn(qn){
        startTimer(60,document.getElementById('timer'));
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
        xhr.send(JSON.stringify({ status: "true" , candidate:"Bob", question: qn }));
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
    xhr.send(JSON.stringify({ status: "false", candidate:"Bob", question:"" }));
}


questions=[
    "Tell me something ",
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec elementum massa in neque rutrum, fringilla venenatis ipsum euismod. Nunc bibendum imperdiet lectus scelerisque tincidunt",
    "3.Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec elementum massa in neque rutrum, fringilla venenatis ipsum euismod. Nunc bibendum imperdiet lectus scelerisque tincidunt"
]

function dispalyQn(qn){
    $(".question h4").html(qn)
}
function process(n){
    $(".nextqn").css("display","none");
    if(questions[parseInt(n)]===undefined){
        window.location.href="/thankyou"
    }else{
        dispalyQn(questions[n]);
        $.when(setTimeout(startQn(parseInt(n)),5000)).then(function(){
            //alert(questions[parseInt(n)]);
            setTimeout(function(){
                $.when(endQn()).then(function(){
                    $(".nextqn").attr("qn",parseInt(n)+1);
                    $(".nextqn").css("display","block");
                });
            },10000);
        });
    }
}

$(".nextqn").click(function(){
    process($(this).attr("qn"));
})


startTimer=function(duration, display) {
    var t=this;
    var timer = duration, minutes, seconds;
    var l=setInterval(function () {
        minutes = parseInt(timer / 60, 10)
        seconds = parseInt(timer % 60, 10);

        minutes = minutes < 10 ? "0" + minutes : minutes;
        seconds = seconds < 10 ? "0" + seconds : seconds;

        display.textContent = minutes + ":" + seconds;

        if (--timer < 0) {
            t.endGame();
            t.actuate();
            clearInterval(l);
        }
    }, 1000);
    
}
