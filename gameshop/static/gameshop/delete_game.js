function delete_game(game_id) {
    $.ajax({
        type: "DELETE",
        beforeSend: function(request) {
            var csrftoken = Cookies.get('csrftoken');
            request.setRequestHeader("X-CSRFToken", csrftoken);
        },
        url: "/studio/"+game_id+"/",
        success: function(data, status, xhttp) {
            document.location.replace('../');
        }
    });
}
