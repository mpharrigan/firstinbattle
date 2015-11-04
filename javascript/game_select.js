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