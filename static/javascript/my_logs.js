$(document).ready(function() {

    function clamp(x) {
        if (x<0) {
            return 0;
        } else if (x>100) {
            return 100;
        } else {
            return x;
        }
    }

    var percent_calories = clamp(100*(total_calories/target_calories));
    var percent_water = clamp(100*(total_water/target_water));
    var percent_sleep = clamp(100*(total_sleep/target_sleep));
    var percent_duration = clamp(100*(total_duration/target_duration));

    var average = ((percent_calories+percent_water+percent_sleep+percent_duration)/4) | 0;

    $("#calorie-dial").css({
        background: "conic-gradient(red 0%, rgb(255, 123, 0) "+percent_calories+"%, transparent "+percent_calories+"%, lightgrey 100%)",
    });
    $("#water-dial").css({
        background: "conic-gradient(aqua 0%, rgb(0, 255, 200) "+percent_water+"%, transparent "+percent_water+"%, lightgrey 100%)",
    });
    $("#sleep-dial").css({
        background: "conic-gradient(rgb(36, 0, 119) 0%, rgb(204, 0, 255) "+percent_sleep+"%, transparent "+percent_sleep+"%, lightgrey 100%)",
    });
    $("#duration-dial").css({
        background: "conic-gradient(rgb(255, 166, 0) 0%, rgb(236, 228, 109) "+percent_duration+"%, transparent "+percent_duration+"%, lightgrey 100%)",
    });

    $("#overall-dial").css({
        background: "conic-gradient(rgb(0, 143, 83) 0%, rgb(0, 255, 136) "+average+"%, transparent "+average+"%, lightgrey 100%)",
    });
    $("#overall-dial .dial-text strong").text(average);
});