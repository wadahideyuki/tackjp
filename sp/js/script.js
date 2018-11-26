$(function(){
	
$(".acrdBox dt").click(function(){
	$(this).toggleClass("opn");
	$(this).next().slideToggle();
	return false;
});

	
	
});
