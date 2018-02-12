function joo() {
    console.log("que");
}
function buy(id) {
    $.ajax({
        type: "GET",
        beforeSend: function(request) {
            var csrftoken = Cookies.get('csrftoken');
            request.setRequestHeader("X-CSRFToken", csrftoken);
        },
        url: "/buy",
        data: {"game_id": id},
        success: function(data, status, xhttp) {
            console.log(data);
            var name = data["name"];
            console.log(name);
            var tag = "#".concat(name);
            $(tag.concat(" input[name=pid]")).val(data["pid"]);
            $(tag.concat(" input[name=checksum]")).val(data["checksum"]);
            $(tag).submit();
            console.log("Submitting form")
        }
    });
}
    

    
    /*function buy(id) {
        $.ajax({
            type: "GET",
            beforeSend: function(request) {
                var csrftoken = Cookies.get('csrftoken');
                request.setRequestHeader("X-CSRFToken", csrftoken);
            },
            url: "/buy",
            data: {"game_id": id},
            success: function(data, status, xhttp) {
                console.log(data);
                //window.location = '/';
            }
        });
        $(".shop_buy").on("click", function () {
        
        });
    }*/

