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
\\
	);

	$('img.a').on("click", sayhi);
	function sayhi () {$( this ).data("clicked",!$(this).data("clicked"));
	if $(this).data("clicked") {
	selectedFilters.push($(this.data('name')))}
	else

	}} //this checks to see if the value of clicked is true. If the value is true, and the image is clicked, it sets to false. If it's false and the image is clicked the value changes to true

});


var selectedFilters = [];
selectedFilters.indexOf($(this.data('name')));
//NOT REAL YET
//if clicked == true (get the name of filter clicked)
////selectedFilters.push($(this.data('name')))



// Autocomplete college name as user types
$( function() {
    $( "#colleges" ).autocomplete({
      source: function (req, response) {
				var results = $.ui.autocomplete.filter(jsCollegeList, req.term);
				response(results.slice(0, 5));  // Limit to 5 results
			}
    });
} );

// Limiting the width of autocomplete
jQuery.ui.autocomplete.prototype._resizeMenu = function () {
  var ul = this.menu.element;
  ul.outerWidth(this.element.outerWidth());
}
