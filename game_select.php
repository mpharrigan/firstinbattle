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
		
		<script type="text/javascript" src="//ajax.googleapis.com/ajax/libs/jquery/1.3/jquery.min.js"></script>
		<script type="text/javascript" src="js/game_select.js"></script>
		<script>

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