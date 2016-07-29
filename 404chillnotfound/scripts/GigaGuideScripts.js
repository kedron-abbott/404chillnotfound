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
	function sayhi () {$( this ).data("clicked",!$(this).data("clicked"));
	}
 //this checks to see if the value of clicked is true. If the value is true, and the image is clicked, it sets to false. If it's false and the image is clicked the value changes to true

	// var selectedFilters = []; //this is the array where the clicked filter names are stored

	$('#filterSubmit').on("click", runThroughAllImgs);//this entire function runs through all the images to check and see which ones are clicked v which ones are not
	function runThroughAllImgs () {
		$('img.a').each(addClicked);
		// console.log (selectedFilters);
		// console.log (radius); //this is how you can check which ones are clicked through the console
//PROBABLY HOW WE ARE GOING TO GET THE INFO INTO THE URL FOR THE MAPS >>> window.location.href="maps.html?filters=" + (selectedFilters).join(",")
		return true;
	}
	function addClicked(index,element){
		if ($(element).data("clicked")) {
			$('<input>').attr({
				type: 'hidden',
				value: true,
				name: $(element).data('name')
			}).appendTo('#filterSubmit')
			//$('#' + $(element).data('name')).val("y");
		  // selectedFilters.push($(element).data('name')); // this puts the clicked filters into the array up top
		}
	}
});



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
};
