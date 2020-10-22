var now = new Date().getTime();
var final = new Date(now.getFullYear(), (now.getMonth() + 1), now.getDate(), now.getHours(), ((now.getMinutes()+15)%60), now.getSeconds()).getTime();

var time_check = setInterval(function() {

    var timeleft = final - now;

    // Calculating the minutes and seconds left
    var minutes = Math.floor((timeleft % (1000 * 60 * 60)) / (1000 * 60));
    var seconds = Math.floor((timeleft % (1000 * 60)) / 1000);

    // Result is output to the specific element
    document.getElementById("timebox").innerHTML = minutes +":"+ seconds;

    // Display the message when countdown is over
  /*  if (timeleft < 0)
  {
    clearInterval(time_check);
    document.getElementById("timebox").innerHTML = "";
  }*/


    }, 1000);
