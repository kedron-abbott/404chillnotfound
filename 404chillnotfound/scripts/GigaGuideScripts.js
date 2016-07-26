$("img.a").hover(
	function() {
    $( this ).stop().animate({"opacity": "0"}, "slow"); // this makes the black and white image look like it disappears
    console.log("fading out: ");
	},
	function() {
    if (!$(this).data("clicked")) { // Checks to see if the value of clicked is false (basically they either never clicked or they unclicked) and if the value is that way, it makes the black and white fade back in
		    $( this ).stop().animate({"opacity": "1"}, "slow");
      	console.log("fading in: ");
     }
	}
);

$('img.a').on("click", sayhi);
function sayhi () {$( this ).data("clicked",!$(this).data("clicked"));} // Checks to see if the value of clicked is true; if the value is true, and the image is clicked, it sets to false; if it's false and the image is clicked, the value changes to true


// Autocomplete college name as user types
$( function() {
    $( "#colleges" ).autocomplete({
      source: jsCollegeList
    });
} );
