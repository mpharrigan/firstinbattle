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
		
		<script type="text/javascript" src="//ajax.googleapis.com/ajax/libs/jquery/1.3/jquery.min.js"></script>
		<script type="text/javascript">
		
		$(document).ready(
			function(){
				
				//If user submits the form
				$("#submitmsg").click(function(){
					var clientmsg = $("#usermsg").val();
					$.post("post.php", {text: clientmsg});				
					$("#usermsg").attr("value", "");
					return false;
				});
				

				
				//Load the file containing the chat log
				function loadLog(){
					var oldscrollHeight = $("#chatbox").attr("scrollHeight") - 20; //Scroll height before the request
					$.ajax({
						url: "chatlog.html",
						cache: false,
						success: function(html){		
							$("#chatbox").html(html); //Insert chat log into the #chatbox div	
							
							//Auto-scroll			
							var newscrollHeight = $("#chatbox").attr("scrollHeight") - 20; //Scroll height after the request
							if(newscrollHeight > oldscrollHeight){
								$("#chatbox").animate({ scrollTop: newscrollHeight }, 'normal'); //Autoscroll to bottom of div
							}				
						},
					});
				}
				
				setInterval (loadLog, 2500);	//Reload file every 2500 ms or x ms if you w
			}
		);
		
		function autoscroll(){
			$("#chatbox").animate({scrollTop:($("#chatbox").attr("scrollHeight") - 20)}, 'normal');
		}
		
		
		</script>
		
		<style>
 	 	 
			 .leftColumn {
				position:fixed;
				float:left;
				background-color:#bac9fd;
				left:0;
				top:0;
				width:35%;
				bottom:0;
				border-style:solid;
				border-width:2px;
			 }
			 
			 .rightColumn {
				position:fixed;
				float:right;
				background-color:#fff;
				right:0;
				top:0;
				width:65%;
				bottom:0;
				border-style:solid;
				border-width:2px;
			 }
			 
			 .headerBar {
				position:static;
				margin-top:5px;
				height:35px;
				width:100%;
				border-bottom-style:solid;
				border-bottom-width:2px;
			 }
			 
			 #openGamesHeader {
				position:absolute;
				text-align:center;
				font-family:"Trebuchet MS", Helvetica, sans-serif;
			 }
			 
			 #openGamesJoinText {
				position:absolute;
				text-align:center;
				line-height:100vh;
				white-space:nowrap;
				width:100%;
			 }
			 
			#nameMessage {
				position:absolute;
				font-family:"Trebuchet MS", Helvetica, sans-serif;
				padding-top:6px;
				padding-left:10px;
			 }
			 
			#changePassword {
				position:relative;
				float:right;
				margin-right:20px;
				font-family:"Trebuchet MS", Helvetica, sans-serif;
				padding-top:6px;
			 }
			 
			 #gameMaker {
				position:relative;
				float:right;
				margin-right:20px;
				font-family:"Trebuchet MS", Helvetica, sans-serif;
				padding-top:6px;
			 }
			 
			#logout {
				position:relative;
				float:right;
				font-family:"Trebuchet MS", Helvetica, sans-serif;
				padding-top:6px;
				margin-right:10px;
			 }
			 
			#wrapper {
				position:absolute;
				padding-bottom:25px;
				background:#EBF4FB;
				border:1px solid #ACD8F0;
				text-align:center;
				padding-left:35px;
				padding-right:35px;
				margin-top:37px;
				right:0;
				bottom:0;
				top:5px;
				left:0;
				
			}
			  
			#chatbox {
				position:absolute;
				bottom:50px;
				top:25px;
				left:25px;
				right:25px;
				text-align:left;
				padding:10px;
				background:#fff;
				border:1px solid #ACD8F0;
				overflow:auto;
			}
			  
			#usermsg {
				width:100%;
				border:1px solid #ACD8F0;
			}
			
			#textwrapper {
				position:absolute;
				bottom:16px;
				right:100px;
				left:37px;
			}
			  
			#submitmsg {
				position:absolute;
				bottom:16px;
				right:37px;
			}
			  
			.error {
				color: #ff0000;
			}
			  
			#menu {
				padding:12.5px 25px 12.5px 25px;
			}
			  
			.msgln {
				margin:0 0 2px 0;
			}
			  
			form {
				margin:0;
				padding:0;
			}
			  
			input {
				font:12px arial;
			}

		</style>
	
	</head>

	<body>
	
	    <div class="leftColumn">
    
        <h2 id="openGamesHeader" class="headerBar">Open Games</h2>
        <span id="openGamesJoinText">Click "Join" to join an available
                                   game</span>
    
    </div>
    
    <div class="rightColumn">
    
        <div class="headerBar">
            <span id="nameMessage">Welcome Back, <?php echo $_SESSION['username'] ?>!</span>
            <a id="logout" href="login.php?status=loggedout">Logout</a>
            <a id="changePassword" href="changepass.php">Change Password</a>
            <?php
                $membership = New Membership();
                if($membership->is_game_maker($_SESSION['username'])) {
                    echo "<a id=\"gameMaker\" href=\"game_select.php\">Create Game</a>";
                }
            ?>
			
			<div id="wrapper">
			
				<div id="menu"><div style="clear:both"></div></div>
		 
				<div id="chatbox">
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
		 
				<form name="message" action="">
					<div id="textwrapper">
						<input name="usermsg" type="text" id="usermsg"/>
					</div>
					<input name="submitmsg" type="submit"  id="submitmsg" value="Send" />
				</form>
			
			</div>
			
			
        </div>
    
    </div>
        
	</body>
</html>
