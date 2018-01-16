 $(document).ready(function() {
            "use strict";
            // Only listens to events, doesn't do anything else for now.
            // Still needs django tags to execute python code for database entries
            var iframe = document.getElementById('game_frame');

            window.addEventListener("message", function(evt) {
                if(evt.data.messageType === "LOAD_REQUEST") {
                    // Load game here
                    console.log("LOAD")
                } else if(evt.data.messageType === "SAVE") {
                    // Saves game to db
                    console.log("SAVE")
                } else if(evt.data.messageType === "SCORE") {
                    // Saves score to highscores
                    console.log("SCORE")
                }
            });

            // simple function to post to iframe, doesn't really do anything yet
            var send_message = function(msg) {
                iframe.contentWindow.postMessage(msg, '*')
            };

        });
