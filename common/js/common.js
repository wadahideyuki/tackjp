$(function(){
	
	//�y�[�W���̃I�[�o�[
	$("img.hover").hover(function(){
	 $(this).fadeTo(100,0.7);
	},function(){
	 $(this).fadeTo(100,1)
	});
	
	$(window).scroll(function(){
		var sclNum = $(window).scrollTop();
		if(sclNum > 100){
			$(".totop").show();
		}else{
			$(".totop").hide();		
		}
	});
	
	//��ƍH��
	$(".flowThumb a").click(function(){
		$(".flowThumb a").removeClass();
		$(this).addClass("selected")
		var flowImg = $(this).attr("href");
		$(".flowPhoto").attr("src",flowImg);
		return false;
	})
	
	//�X�N���[��
	$(".scl").click(function(){
		var speed = 400;// �~���b
		var href= $(this).attr("href");
		var target = $(href == "#" || href == "" ? 'html' : href);
		var position = target.offset().top;
		$($.browser.safari ? 'body' : 'html').animate({scrollTop:position}, speed, 'swing');
	})
	
	
	
})