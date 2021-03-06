//handle adding and removing alarms
function loadAlarms(){
    var contain = $('#current');
    $.get("../get_alarms", function(content){
        var data = $.parseJSON(content);
        for( x in data){
            contain.append(data[x] + "<br/>");
        }
    });
}


//add new alarm
$("#newbutton").click(function(event){
    var day = "";
    if($("#M").is(":checked")){
        day = day + "M";
    }
    if($("#T").is(":checked")){
        day = day + "T";
    }
    if($("#W").is(":checked")){
        day = day + "W";
    }
    if($("#R").is(":checked")){
        day = day + "R";
    }
    if($("#F").is(":checked")){
        day = day + "F";
    }
    if($("#S").is(":checked")){
        day = day + "S";
    }
    if($("#U").is(":checked")){
        day = day + "U";
    }

//get alarm sound
    console.log( "day is " + day + ".");

    var timeval = $("#ATIME").val();
    console.log( "time is " + timeval + ".");

    var soundval = $("#sounds option:selected").text();
    console.log( "sound is " + soundval + ".");

    var newalarm = day + "-" + timeval + "-" + soundval;
    console.log( "full string is " + newalarm);
    $.get("../set_alarm/"+newalarm, function(data){
        console.log(data);
    });
});

