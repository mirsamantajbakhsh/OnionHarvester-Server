/**
 * Created by mohammad on 12/16/17.
 */

function countUp(){
    var records = document.getElementsByClassName("pool");
    var timeout = document.getElementById("timeout");
    for(var i = 0; i < records.length; i++)
    {
        var minute = 0;
        if(records.item(i).getElementsByClassName('timeout')[0].innerHTML != "-") {
            minute = setTime(records.item(i));
        }
        if(minute >29){
            records.item(i).getElementsByClassName('timeout')[0].innerHTML = "-";
            records.item(i).style.color = "red";
        }
    }
}
setInterval(countUp, 1000);

function setTime(record) {
    var temp = record.getElementsByClassName('timeout')[0].innerHTML.split(":");
    var totalSeconds = parseInt(temp[0]) * 60 + parseInt(temp[1]) + 1;
    var minutes = pad(parseInt(totalSeconds / 60));
    var seconds = pad(totalSeconds % 60);
    record.getElementsByClassName('timeout')[0].innerHTML = minutes + ":" + seconds;
    return minutes;

}

function pad(val) {
  var valString = val + "";
  if (valString.length < 2) {
    return "0" + valString;
  } else {
    return valString;
  }
}