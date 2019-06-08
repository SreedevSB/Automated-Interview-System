


var buttonRecord = document.getElementById("record");
var buttonStop = document.getElementById("stop");

buttonStop.disabled = true;

buttonRecord.onclick = function() {
    process(0);
    buttonRecord.style.display="none"
};

buttonStop.onclick = function() {
    endQn()
};



var url_string = window.location.href
var url = new URL(url_string);
var cname = url.searchParams.get("name");

function startQn(qn){
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
        xhr.send(JSON.stringify({ status: "true" , candidate:cname , question: qn }));
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
    xhr.send(JSON.stringify({ status: "false", candidate:cname, question:"" }));
}


questions=[
    "Do you have philosophy in life?",
    "You don’t have enough experience for this position. Tell me why my client should hire you.",
    "Think of a time when you set a goal that you didn’t reach. Why didn’t you reach it? How did you handle it?",
    "Please provide us an example of a work situation that really stressed you out to the max?",
    "Why should I hire an outsider like you when I could fill this position with someone in our company who is familiar with our culture and products?"
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
        $(".timer .count").html(10);
        $.when(setTimeout(startQn(parseInt(n)),5000)).then(function(){
            //alert(questions[parseInt(n)]);
            //=startTimer(30,document.getElementById('timer'));
            ct=9;
            st=setInterval(function (){if(ct!=-1){$(".timer .count").html(ct--);}else{clearInterval(st);}},1000);

            setTimeout(function(){
                $.when(endQn()).then(function(){
                    $(".nextqn").attr("qn",parseInt(n)+1);
                    $(".nextqn").css("display","inline-block");
                });
            },10000);
        });
    }
}

$(".nextqn").click(function(){
    process($(this).attr("qn"));
})
/*
document.onload=function(){
startTimer=function(duration, display) {
    var t=this;
    var timer = duration, minutes, seconds;
    var l=setInterval(function () {
        minutes = parseInt(timer / 60, 10)
        seconds = parseInt(timer % 60, 10);

        minutes = minutes < 10 ? "0" + minutes : minutes;
        seconds = seconds < 10 ? "0" + seconds : seconds;

        display.textContent = minutes + ":" + seconds;

        if (--timer <= 0) {
            t.endGame();
            t.actuate();
            clearInterval(l);
        }
    }, 1000);

}
}*/
