$( document ).ready(function() {
	$("img.a").hover(
		function() {
	    $( this ).stop().animate({"opacity": "0"}, "fast"); // this makes the black and white image look like it disapears. (i know i spelled disappears wrong, but i dont care to change it rn)
	    console.log("fading out: ");
		},
		function() {
	    if (!$(this).data("clicked")) { //this part checks to see if the value of clicked is false (basically the either never clicked or they unclicked) and if the value is that way, it makes the black and white fade back in.
			    $( this ).stop().animate({"opacity": "1"}, "fast");
	      	console.log("fading in: ");
	     }
		}
	);

	$('img.a').on("click", sayhi);
	function sayhi () {$( this ).data("clicked",!$(this).data("clicked"));} //this checks to see if the value of clicked is true. If the value is true, and the image is clicked, it sets to false. If it's false and the image is clicked the value changes to true

});









//Below is Savannah's code -- this is the autocomplete feature on the site

//$( function() {
//    $( "#colleges" ).autocomplete({
//      source: jsCollegeList
//    });
//  } );
/*
var options = {
	data: jsCollegeList
	placeholder: "College Name"
	getValue: "name",
	list: {
		match: {
			enabled: true
		},
		maxNumberOfElements: 8
	},
	theme: "plate-dark"
};

$("#plate").easyAutocomplete(options);
*/
