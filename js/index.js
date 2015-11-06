$(document).ready(
	function(){
		
		//If user submits the form
		$("#loginSubmitMsg").click(function(){
			var clientmsg = $("#loginUserMsg").val();
			$.post("post.php", {text: clientmsg});				
			$("#loginUserMsg").attr("value", "");
			return false;
		});
		

		
		//Load the file containing the chat log
		function loadLog(){
			var oldscrollHeight = $("#loginChatbox").attr("scrollHeight") - 20; //Scroll height before the request
			$.ajax({
				url: "chatlog.html",
				cache: false,
				success: function(html){		
					$("#loginChatbox").html(html); //Insert chat log into the #loginChatbox div	
					
					//Auto-scroll			
					var newscrollHeight = $("#loginChatbox").attr("scrollHeight") - 20; //Scroll height after the request
					if(newscrollHeight > oldscrollHeight){
						$("#loginChatbox").animate({ scrollTop: newscrollHeight }, 'normal'); //Autoscroll to bottom of div
					}				
				},
			});
		}
		
		setInterval (loadLog, 2500);	//Reload file every 2500 ms or x ms if you w
	}
);

function autoscroll(){
	$("#loginChatbox").animate({scrollTop:($("#loginChatbox").attr("scrollHeight") - 20)}, 'normal');
}