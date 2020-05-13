$(function () {
	$('#nom').autocomplete({
	  minLength: 2,
	  source: "readDirectory.php"
	});
  });