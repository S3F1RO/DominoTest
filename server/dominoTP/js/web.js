$(document).ready(function(){
//==============================================================================





/*==============================================================================
  jQuery events
==============================================================================*/

  // Change wrapper and <li> color on wrapper dblclick
  jQuery("body").on("dblclick", ".wrapper", function() {
    jQuery(this).css("background-color", "pink");
    jQuery("li").css("background-color", "yellow");
  });

//==============================================================================
});
