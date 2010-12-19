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
			twttr.mediaType("twttr.media.types.Chattify", {
				icon: "generic", 
				domain: "http://chattify.appspot.com", 
				matchers: {
					media:/chattify.appspot.com\/chat\/([a-zA-Z0-9\.]+)/g
				},
				process: function(next) {
					// if link is http://imgur.com, ext usually missing
					if( this.slug.indexOf('.') < 0 ) 
						this.slug = this.slug;
					this.data.src = this.slug;
					this.data.name = this.constructor._name;
					this.data.channel = this.tweet.id;
					this.data.name = $('#screen-name').html().replace(/^\s+|\s+$/g, '');
					next()
				},
				render:function(el) {
					var markup = "<iframe src='http://chattify.appspot.com/chat/{src}/{name}' scrolling='no' style='width:370px; height:500px' frameborder='0'></iframe>";
					$(el).append(twttr.supplant(markup,this.data))
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