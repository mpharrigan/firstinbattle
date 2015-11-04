<?php

require_once 'classes/Membership.php';

if (isset($_POST['games'])) {
    echo "yes";
}

?>

<!DOCTYPE html>
<html>
	<head>
		<title>Choose Game</title>
		
		<meta charset="UTF-8" />
		<meta http-equiv="Content-type" content="text/html; charset=utf-8" />
		<meta name="viewport" content="width=device-width, initial-scale=1" />
		
		<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
		<script>
		
            $(document).ready(
                function() {
                    $("#game").on("change",function() {
                        $.post("players_allowed.php", {game_name: $("#game option:selected").text()}, function(data){
                                alert(data);/*
                                var min = data[0];
                                var max = data[1];
                                var set_num_rounds = data[2];
                                $("#num_players").empty();
                                for (i = min; i < max + 1; i++) {
                                    $("#num_players").append("<option>" + i + "</option>");
                                }
                                if (set_num_rounds) {
                                    $("#num_players").attr("readonly",true);
                                } else {
                                    $("#num_players").attr("readonly",false);
                                }*/
                            }
                    );
                }
            );
            });
        
        </script>

	</head>

	<body>
	
		<div>
			<form method="post" action="">
			    <h4>Select game:</h4>
				<select id="game" name="game">
				    <?php
				        $membership = new Membership();
				        $membership->get_game_names();
				    ?>
				</select>
				<h4>Select number of players:</h4>
				<select id="num_players" name="num_players">
				</select>
				<h4>Select number of rounds:</h4>
				<input type="text" id="num_players" name="rounds">
			</form>
		</div>        
	</body>
</html>