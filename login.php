<?php
session_start();
require_once 'classes/Membership.php';
$membership = new Membership();

// If the user clicks the logout link on the index page
if(isset($_GET['status']) && $_GET['status'] == 'loggedout') {
	$membership->log_User_Out();
}

// Did the user enter a password/username and click submit?
if($_POST && !empty($_POST['username']) && !empty($_POST['password'])) {
	$response = $membership->validate_User($_POST['username'], $_POST['password']);
}

?>

<!DOCTYPE html>
<html>
	<head>
		<title>First In Battle Login</title>
		
		<meta charset="UTF-8" />
		<meta http-equiv="Content-type" content="text/html; charset=utf-8" />
		<meta name="viewport" content="width=device-width, initial-scale=1" />
	    
		<link rel="stylesheet" type="text/css" href="css/style.css" />

	</head>

	<body>
	
		<div id="login">
			<form method="post" action="">
				<div class="body"></div>
				<div class="grad"></div>
				<div class="header">
					<div>Let's<span>Play</span></div>
				</div>
				<br>
				<div class="login">
					<input type="text" placeholder="username" name="username" /><br>
					<input type="password" placeholder="password" name="password" /><br>
					<input type="submit" id="submit" value="Login" name="submit" /><br>
					<?php if(isset($response)) echo "<h4>" . $response . "</h4>"; ?>
				</div>
			</form>
		</div>
        
	</body>
</html>
