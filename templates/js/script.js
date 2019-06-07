(function() {
	// body...
	//variable
	var documentElem = $(document),
		projectVisibleContents = $('.project-visible'),
		projectExtraToggleBtn  = projectVisibleContents.find('.project-extra-toggle'),
		nav = $('nav'),
		navigateElems = $('nav li a, .continue-btn'),
		htmlBody = $('html, body'),
		lastScrolltop=0,
		introBg = $('.intro'),
		login= $('.login'),
		logintb= $('.login-reg-panel'),
		home= $('.intro-heading');
 
 	//toggle nav bar
		documentElem.on('scroll', function() { 
			var currentScrolltop=$(this).scrollTop();
			(currentScrolltop > lastScrolltop) ? nav.addClass('hidden') : nav.removeClass('hidden');
			lastScrolltop=currentScrolltop;
		})

	//nav menue
		navigateElems.on('click', function(e){
			if($(this).data('scroll-target')!='none'){
				var targetElem =$( $(this).data('scroll-target') ),
					targetoffsetTop = targetElem.offset().top;

					htmlBody.animate({
						scrollTop:targetoffsetTop
					},400);

					e.preventDefault();
			}

		});

	//project slide
		projectExtraToggleBtn.on('click', function(e){
			var self = $(this),
			closestExtra = self.closest('.pro').find('.project-extra');
			closestExtra.slideToggle(400,function(){

				( closestExtra.is(':visible')) ? self.text('less') : self.text('More');
			});

			e.preventDefault();
		});


	// parallax effect

		documentElem.on('scroll', function() {
			var currentScrolltop = $(this).scrollTop();
			introBg.css('background-position', '50% ' + -currentScrolltop/4 + 'px');

		});

		login.on('click', function(e){

			logintb.addClass('fadein');
			home.addClass('fadeout');
			nav.addClass('fadeout');
		});

		$('.close').on('click', function(e){

			logintb.addClass('fadeout');
			home.addClass('fadein');
			nav.addClass('fadein');
		});


})();