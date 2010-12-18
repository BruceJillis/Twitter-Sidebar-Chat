// ==UserScript==
// @name          Twitter Sidebar Chat
// @namespace     http://chattify.appspot.com/
// @description   A simple extension for #newtwitter that adds a chat as a new mediatype
// @include       http://twitter.com/*
// @include       https://twitter.com/*
// @run_at        document_end
// ==/UserScript==

(function(){
	// this function gets injected into the "main" DOM as a script tag
	function payload() {
		// main "script" logic
		var handler = function() {
			// has the twttr object been created?
			if( twttr == undefined )
				setTimeout(handler, 500); // sleep a bit and try again
			// yay, we have access, add our modifications
			debugger;
			twttr.mediaType("twttr.media.types.Chattify", {
				icon: "generic", 
				domain: "http://chattify.appspot.com", 
				matchers: {
					media:/imgur.com\/([a-zA-Z0-9\.]+)/g
				},
				/*
				process: function(next) {					
					// if link is http://imgur.com, ext usually missing
					if( this.slug.indexOf('.') < 0 ) 
						this.slug = this.slug + '.jpg';
					this.data.src = this.slug;
					this.data.name = this.constructor._name;
					next()
				},
				*/
				render:function(el) {
					//var markup = '<div class="twitpic"><a class="inline-media-image" data-inline-type="{name}" href="http://i.imgur.com/{src}" target="_blank"><img src="http://i.imgur.com/{src}" /></a>';                
					markup = "<iframe src='http://cw.gabbly.com/gabbly/cw.jsp?e=1&t=twitter.com' scrolling='no' style='width:300px; height:250px' frameborder='0'></iframe>";
					$(el).append(twttr.supplant(A,this.data))
				}
		});
		}
		setTimeout(handler, 500);
	}
	
	// inject the script into the DOM of the main page
	var script = document.createElement('script');
	script.appendChild(document.createTextNode('('+ payload +')();'));
	document.body.appendChild(script);
})();