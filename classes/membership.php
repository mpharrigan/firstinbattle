<?php

require 'Mysql.php';

class Membership {

	function validate_user($un, $pwd) {
		$mysql = New Mysql();
		$ensure_credentials = $mysql->verify_Username_and_Pass($un, hash("md5",$pwd));
		
		if($ensure_credentials) {
			$_SESSION['status'] = 'authorized';
			$_SESSION['username'] = $un;
			
			$fp = fopen("chatlog.html", 'a');
			fwrite($fp, "<div class='msgln'>(".date("g:i A").") <i>". $_SESSION['username'] ." has joined the chat session.</i><br></div>");
			fclose($fp);
			
			header("location: index.php");
		} else return "Please enter a correct username and password.";
	}
	
	function log_User_Out() {
		if(isset($_SESSION['status'])) {
			$fp = fopen("chatlog.html", 'a');
			fwrite($fp, "<div class='msgln'>(".date("g:i A").") <i>". $_SESSION['username'] ." has left the chat session.</i><br></div>");
			fclose($fp);
	
			unset($_SESSION['status']);
			if(isset($_COOKIE[session_name()])) setcookie(session_name(), '', time() - 10000);
			session_destroy();
		}
	}
	
	function confirm_Member() {
		session_start();
		if($_SESSION['status'] !='authorized') header("location: login.php");
	}
	
	function change_pass($old_pass, $new_pass) {
		$mysql = New Mysql();
		$password_changed = $mysql->change_Password($_SESSION['username'], hash("md5",$old_pass), hash("md5",$new_pass));
		
		if($password_changed) {
			return "Password successfully changed!";
		} else return "Something went wrong when trying to change your password...";
	}
	
	function is_game_maker ($un) {
	    $mysql = New Mysql();
	    return $mysql->game_maker($un);
	}
	
	function get_game_names() {
	    $mysql = New Mysql();
	    $mysql->acquire_game_names();
	}
	
	function get_min_players($game) {
	    $mysql = New Mysql();
	    return $mysql->acquire_game_min($game);
	}

}

?>