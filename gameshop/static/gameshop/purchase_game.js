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
            //console.log(data);
            var name = data["name"];
            //console.log(name);
            var tag = "#".concat(name);
            var form = $(document.getElementById(data["name"]));
            //console.log(form);
            var pid = form.find("input[name=pid]");
            pid.val(data["pid"]);
            //console.log(pid);
            var checksum = form.find("input[name=checksum]");
            checksum.val(data["checksum"]);
            //console.log(checksum);
            
            //$(tag.concat(" input[name=pid]")).val(data["pid"]);
            //$(tag.concat(" input[name=checksum]")).val(data["checksum"]);
            var path = String(window.location);
            var homepath = path.substring(0, (path.length - 5))
            var success_path = homepath.concat("payment/success/");
            var cancel_path = homepath.concat("payment/cancel/");
            var error_path = homepath.concat("payment/error/");
            
            form.find("input[name=success_url]").val(success_path);
            form.find("input[name=cancel_url]").val(cancel_path);
            form.find("input[name=error_url]").val(error_path);
            form.submit();
            //console.log("Submitting form")
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

