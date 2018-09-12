$(document).ready(function() {

  var url = new URL(document.location);

  var params = url.searchParams;
  var section = params.get("section");

  $('.section_option').filter(function() { 
        return ($(this).text() == section);
    }).prop('selected', true);

});