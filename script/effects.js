$(document).ready(function(){

	$("h2").mouseover(function(){

		$("h2").fadeTo('fast',1);

	});

	$("h2").mouseleave(function(){

		$("h2").fadeTo('fast',0.5);

	});
})