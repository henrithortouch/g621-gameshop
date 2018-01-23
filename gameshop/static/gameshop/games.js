$("#show").click( function() {
    var a = $.ajax({
        type: "SHOW_GAMES",
        beforeSend: function(request) {
            request.setRequestHeader("X-CSRFToken", document.getElementsByName('csrfmiddlewaretoken')[0].value);
          },
        url: "/games",
        data: "",
        success: null,
        dataType: ""
    });
    
    console.log({csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value})
    console.log(a)
    console.log("ok")
});