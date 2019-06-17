$(function(){
	$('#cilck_menu').click(function(){
        if($('#hidden_part').is(':hidden')) {
          $('#hidden_part').slideDown();  
        } else {
          $('#hidden_part').slideUp();
        }
	});
	});