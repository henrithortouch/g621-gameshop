 $(document).ready(function() {
            "use strict";
            var iframe = document.getElementById('game_frame')

            window.addEventListener("message", function(evt) {
                if(evt.data.messageType === "LOAD_REQUEST") {
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
                            if (status === 200){
                                console.log("SUCCESS")
                            } else {
                                console.log(data)
                                console.log("FAILURE")
                            }
                            
                        },
                    });
                    // Saves score to highscores
                    console.log("SCORE")
                }
            });

            // simple function to post to iframe, doesn't really do anything yet
            var send_message = function(msg) {
                iframe.contentWindow.postMessage(msg, '*')
            };

        });
