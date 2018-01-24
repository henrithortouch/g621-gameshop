$(document).ready(function () {
    $("#show").on("click", function(event) {
        
        // Prevent the default behaviour e.g. re-rendering of page
        event.preventDefault();
        
        var a = $.ajax({
            type: "GET",
            beforeSend: function(request) {
                request.setRequestHeader("X-CSRFToken", document.getElementsByName('csrfmiddlewaretoken')[0].value);
              },
            success: function(data, status, xhttp) {
                console.log(data)
                $("#list").append(data)
            }
        });
        
        console.log({csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value})
        console.log("ok")
    });
});
