 $(document).ready(function() {
            "use strict";
            // Only listens to events, doesn't do anything else for now.
            // Still needs django tags to execute python code for database entries
            var iframe = document.getElementById('game_frame')

            window.addEventListener("message", function(evt) {
                if(evt.data.messageType === "LOAD_REQUEST") {
                    console.log("LOAD")

                } else if(evt.data.messageType === "SAVE") {
                    var state = evt.data.gameState
                    var json = JSON.stringify(state)
                    var msg = {
                        "message_type": "SAVE_REQUEST",
                        "game_state": state,
                        //"u_id" : u_id
                    }
                    console.log(JSON.stringify(msg))
                    console.log(window.location + "save_state/")
                    // Posts to this fucking window get a better function
                    //var response = window.postMessage(msg, window.location + "save_state/")
                    console.log(response)
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
