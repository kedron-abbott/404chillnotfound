$("img.a").hover(
	function() {
		$( this ).stop().animate({"opacity": "0"}, "slow");
    console.log("fading out: ");
	},
	function() {
		$( this ).stop().animate({"opacity": "1"}, "slow");
    console.log("fading in: ");
	}
);
