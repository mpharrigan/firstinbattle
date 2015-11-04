<?php

require_once 'classes/Membership.php';
$membership = New Membership();

$membership->confirm_Member();

// Did the user enter a password and click submit?
if($_POST && !empty($_POST['curr_pass']) && !empty($_POST['new_pass'])) {
	$response = $membership->change_pass($_POST['curr_pass'], $_POST['new_pass']);
}
?>

<!DOCTYPE html>
<html>
	<head>
		<title>Change Password</title>
		
		<meta charset="UTF-8" />
		<meta http-equiv="Content-type" content="text/html; charset=utf-8" />
		<meta name="viewport" content="width=device-width, initial-scale=1" />
	
	</head>

	<body>
	
		<div>
			<form method="post" action="">
				Current password: <input type="password" placeholder="Current Password" name="curr_pass" /><br>
				New password: <input type="password" placeholder="New Password" name="new_pass" /><br>
				<input type="submit" value="Change" name="submit" /><br>
				<?php if(isset($response)) echo "<h4>" . $response . "</h4>"; ?>
			</form>
			<br>
			<p>
				<a href="index.php">Go Home</a>
			</p>
		</div>
        
	</body>
</html>