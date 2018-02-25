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

            var name = data["name"];

            var tag = "#".concat(name);
            var form = $(document.getElementById(data["name"]));

            var pid = form.find("input[name=pid]");
            pid.val(data["pid"]);

            var checksum = form.find("input[name=checksum]");
            checksum.val(data["checksum"]);

            var path = String(window.location);
            var homepath = path.substring(0, (path.length - 5))
            var success_path = homepath.concat("payment/success/");
            var cancel_path = homepath.concat("payment/cancel/");
            var error_path = homepath.concat("payment/error/");
            
            form.find("input[name=success_url]").val(success_path);
            form.find("input[name=cancel_url]").val(cancel_path);
            form.find("input[name=error_url]").val(error_path);
            form.submit();
        }
    });
}
