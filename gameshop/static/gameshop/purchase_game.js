$(document).ready(function (){
    $(".shop_buy").on("click", function () {

        var price = $(this).siblings("#game_price").text().trim().split(" ");
        console.log(price[1]); //The current price
        var json_data = {"price": price[1]};
        $.ajax({
            type: "GET",
            beforeSend: function(request) {
                var csrftoken = Cookies.get('csrftoken');
                request.setRequestHeader("X-CSRFToken", csrftoken);
            },
            success: function(data, status, xhttp) {
                console.log(data);
                //window.location = '/';
            }
        })
    });
});
