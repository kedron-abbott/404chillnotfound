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

$( function() {
    $( "#colleges" ).autocomplete({
      source: jsCollegeList
    });
  } );
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
