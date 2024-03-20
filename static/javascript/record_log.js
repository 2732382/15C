$(document).ready(function() {
    $("LogForm").on("submit", function(event){
        event.preventDefault(); // Prevent default form submission

        var formData = {
            'water': $('#id_water').val(),
            'calories': $('#id_calories').val(),
            'sleep': $('#id_sleep').val(),
            'activity_name': $('#activity_name').val(),
            'activity_duration': $('#activity_duration').val(),
            'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
        };

        $.ajax({
            type: "POST",
            url: "/renova/my-logs/", // URL to your Django view
            data: formData,
            success: function(response) {
                console.log("Log successfully recorded.");
                // Optionally, redirect to my_logs page or update the UI accordingly
            },
            error: function(response) {
                console.log("Error recording log.");
            }
        });
    });
});
