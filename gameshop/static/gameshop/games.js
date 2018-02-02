$(document).ready(function () {
    $("#show").on("click", function(event) {
        
        // Prevent the default behaviour e.g. re-rendering of page
        event.preventDefault();
        
        $.ajax({
            type: "GET",
            beforeSend: function(request) {
                request.setRequestHeader("X-CSRFToken", document.getElementsByName('csrfmiddlewaretoken')[0].value);
              },
            success: function(data, status, xhttp) {
                console.log(data)
                $("#list").replaceWith(data)
            }
        });
        
        console.log({csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value})
        console.log("ok")
    });
    
    $("#money").on("click", function(event) {
        
        // Prevent the default behaviour e.g. re-rendering of page
        event.preventDefault();
        
        $.ajax({
            type: "ADD_MONEY",
            beforeSend: function(request) {
                request.setRequestHeader("X-CSRFToken", document.getElementsByName('csrfmiddlewaretoken')[0].value);
              },
            success: function(data, status, xhttp) {
                //$("#money").replaceWith(data)
            }
        });
        
        console.log({csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value})
        console.log("ok")
    });
});
