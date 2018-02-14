 $(document).ready(function() {
            "use strict";
            var iframe = document.getElementById('game_frame')

            window.addEventListener("message", function(evt) {
                if(evt.data.messageType === "LOAD_REQUEST") {
                    var response = $.ajax({
                        type: "GET",
                        beforeSend: function(request) {
                            request.setRequestHeader("X-CSRFToken", document.getElementsByName('csrfmiddlewaretoken')[0].value);
                        },
                        url: window.location + "load/",
                        success: function(data, status, xhttp) {
                            console.log(status)
                            if (status === "success"){
                                console.log(data)
                                var obj = JSON.parse(data)
                                var message = {
                                    messageType: "SAVE",
                                    gameState: obj,
                                }
                                console.log(obj)
                            }
                        },
                    });
                    console.log("LOAD")
                } else if(evt.data.messageType === "SAVE") {
                    var msg = evt.data.gameState
                    console.log(msg)
                    var response = $.ajax({
                        type: "POST",
                        beforeSend: function(request) {
                            request.setRequestHeader("X-CSRFToken", document.getElementsByName('csrfmiddlewaretoken')[0].value);
                        },
                        url: window.location + "save/",
                        data: msg,
                        success: function(data, status, xhttp) {
                            //TODO: Send error to iframe if not success
                            console.log("SUCCESS")
                        },
                    });
                    //var response = window.postMessage(msg, window.location + "save_state/")
                    console.log("SAVE")

                } else if(evt.data.messageType === "SCORE") {
                    var score = evt.data.score
                    var response = $.ajax({
                        type: "POST",
                        beforeSend: function(request) {
                            request.setRequestHeader("X-CSRFToken", document.getElementsByName('csrfmiddlewaretoken')[0].value);
                        },
                        url: window.location + "score/",
                        data: {score: score},
                        success: function(data, status, xhttp) {
                            if (status === "success"){
                                console.log("SUCCESS")
                            } else {
                                //TODO: Send error to iframe
                                console.log(data)
                                console.log("FAILURE")
                            }
                        },
                    });
                    // Saves score to highscores
                    console.log("SCORE")
                } else if(evt.data.messageType === "SETTING"){
                    $("#game_frame").attr("width", evt.data.options.width)
                    $("#game_frame").attr("height", evt.data.options.height)
                } // else do nothing, maybe send a error to iframe?
            });

            // simple function to post to iframe, doesn't really do anything yet
            var send_message = function(msg) {
                iframe.contentWindow.postMessage(msg, '*')
            };

        });
