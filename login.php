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
<html lang="en">
	<head>		
		<meta charset="utf-8">
		<meta http-equiv="X-UA-Compatible" content="IE=edge">
		<meta name="viewport" content="width=device-width, initial-scale=1">
		
		<!-- The above 3 meta tags *must* come first in the head; any other head content must come *after* these tags -->
		<title>First In Battle Login</title>
		
		<!-- Bootstrap -->
		<link href="css/bootstrap.min.css" rel="stylesheet">
		
		<!-- HTML5 shim and Respond.js for IE8 support of HTML5 elements and media queries -->
		<!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
		<!--[if lt IE 9]>
			<script src="https://oss.maxcdn.com/html5shiv/3.7.2/html5shiv.min.js"></script>
			<script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
		<![endif]-->
		
		<link rel="stylesheet" type="text/css" href="css/style.css" />

	</head>

	<body id="loginBody">
			<form method="post" action="">
				<div id="loginContainer"></div>
				<div id="loginGrad"></div>
				<div class="vertical-centering">
					<div class="container">
						<div class="row">
							<div class="col-md-1 "></div><div class="col-md-1 "></div><div class="col-md-1 "></div>
							<div id="loginHeader" class="col-md-1">Let's<span id="login-header-span">Play</span></div><div class="col-md-1 "></div>
							<div id="loginBoxes" class="col-md-4">
								<input type="text" placeholder="username" name="username" class="login-textbox" /><br>
								<input type="password" placeholder="password" name="password" class="login-textbox" /><br>
								<input type="submit" id="submit" value="Login" name="submit" /><br>
								<?php if(isset($response)) echo "<h4 id=\"loginFail\">" . $response . "</h4>"; ?>
							</div>
							<div class="col-md-1 "></div><div class="col-md-1 "></div><div class="col-md-1 "></div>
						</div>
					</div>
				</div>
			</form>
		
        <!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
		<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
		<!-- Include all compiled plugins (below), or include individual files as needed -->
		<script src="js/bootstrap.min.js"></script>
	</body>
</html>