<?php

require_once 'includes/constants.php';

class Mysql {
	private $conn;
	
	function __construct() {
		$this->conn = new mysqli(DB_SERVER, DB_USER, DB_PASSWORD, DB_NAME) or die('There was a problem connecting to the database.');
	}
	
	function verify_Username_and_Pass($un, $pwd) {
		
		$query = "SELECT *
				  FROM users
				  WHERE username = ? AND password = ?
				  LIMIT 1";
				  
		if($stmt = $this->conn->prepare($query)) {
			$stmt->bind_param('ss', $un, $pwd);
			$stmt->execute();
			
			if($stmt->fetch()) {
				$stmt->close();
				return true;
			}
		}
	}
	
	function change_Password($un, $current_pass, $new_pass) {
		$query = "UPDATE users
				  SET password = ?
				  WHERE username = ? AND password = ?";
				  
		if($stmt = $this->conn->prepare($query)) {
			$stmt->bind_param('sss', $new_pass, $un, $current_pass);
			$stmt->execute();
			
			if(mysqli_affected_rows($this->conn)) {
				$stmt->close();
				return true;
			}
		}
	}
	
	function game_maker($un) {
	    $query = "SELECT * FROM users where username = ? AND game_maker = 1 LIMIT 1";
	    
	    if($stmt = $this->conn->prepare($query)) {
			$stmt->bind_param('s', $un);
			$stmt->execute();
			
			if($stmt->fetch()) {
				$stmt->close();
				return true;
			}
		}
	}
	
	function acquire_game_names() {
	    $query = "SELECT name FROM games";
	    
	    $result = $this->conn->query($query);
	    
	    $num_rows = $result->num_rows;
	    
	    if($num_rows == 0)
	    {
	        echo "<h3>No items are currently in the games table</h3>\n";
	    } else {
	        echo "<option selected=\"selected\" disabled=\"disabled\">Select a game</option>\n";
            while ($row = $result->fetch_array())
            {
                echo "<option value=\"$row[0]\">$row[0]</option>";
            }
            echo "</select>";
            $result->free();
	    }
	    
	    $result->close();
    }
    
    function acquire_game_min($game_name) {
        $query = "SELECT min_players FROM games WHERE name = $game_name LIMIT 1";
        $result = $this->conn->query($query);
        $number = $result->fetch_array();/*
        $result->close();*/
        return 1;
    }
    
    function acquire_game_max($game_name) {
        $query = "SELECT max_players FROM games WHERE name = $game_name LIMIT 1";
        $result = $this->conn->query($query);
        $number = $result->fetch_array();
        $result->close();
        return $number;
    }
    
    function set_num_rounds($game_name) {
        $query = "SELECT set_num_rounds FROM games WHERE name = $game_name LIMIT 1";
        $result = $this->conn->query($query);
        $number = $result->fetch_array();
        $result->close();
        return $number;
    }
	
}

?>