<?php

require_once 'classes/Membership.php';
$membership = New Membership();

$membership->confirm_Member();
?>



<!DOCTYPE html>
<html>
	<head>
		<title>First In Battle Home</title>
		<meta charset="UTF-8" />
		<meta http-equiv="Content-type" content="text/html; charset=utf-8" />
		<meta name="viewport" content="width=device-width, initial-scale=1" />
		
		<link rel="stylesheet" type="text/css" href="css/style.css" />
		
		<script type="text/javascript" src="//ajax.googleapis.com/ajax/libs/jquery/1.3/jquery.min.js"></script>
		<script type="text/javascript" src="js/index.js"></script>
	
	</head>

	<body>
	
	    <div id="indexLeftColumn">
    
        <h2 id="indexOpenGamesHeader" class="indexHeaderBar">Open Games</h2>
        <span id="indexOpenGamesJoinText">Click "Join" to join an available
                                   game</span>
    
    </div>
    
    <div id="indexRightColumn">
    
        <div class="indexHeaderBar">
            <span id="indexNameMessage">Welcome Back, <?php echo $_SESSION['username'] ?>!</span>
            <a id="indexLogout" href="login.php?status=loggedout">Logout</a>
            <a id="indexChangePassword" href="changepass.php">Change Password</a>
            <?php
                $membership = New Membership();
                if($membership->is_game_maker($_SESSION['username'])) {
                    echo "<a id=\"indexGameMaker\" href=\"game_select.php\">Create Game</a>";
                }
            ?>
			
			<div id="loginWrapper">
			
				<div id="loginMenu"><div style="clear:both"></div></div>
		 
				<div id="loginChatbox">
					<?php
						if(file_exists("chatlog.html") && filesize("chatlog.html") > 0){
							$handle = fopen("chatlog.html", "r");
							$contents = fread($handle, filesize("chatlog.html"));
							fclose($handle);
							 
							echo $contents;
						}
					?>
					<script type="text/javascript">
						autoscroll();
					</script>
				</div>
		 
				<form name="message" action="" id="indexForm">
					<div id="loginTextWrapper">
						<input name="usermsg" type="text" id="loginUserMsg"/>
					</div>
					<input name="submitmsg" type="submit"  id="loginSubmitMsg" value="Send" />
				</form>
			
			</div>
			
			
        </div>
    
    </div>
        
	</body>
</html>
