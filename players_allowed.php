<?php

    require_once 'classes/Mysql.php';
    session_start();
    
    if(isset($_SESSION['username'])){
        $game = $_POST['game_name'];
        $mysql = New Mysql();
        $min = $mysql->acquire_game_min($game);/*
        $max = $mysql->acquire_game_max($game);
        $num_rounds = $mysql->set_num_rounds($game);
        $array = array($min, $max, $num_rounds);*/
        echo "hi";
        /*echo json_encode($array);*/
    }
?>