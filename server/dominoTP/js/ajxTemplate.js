  $(document).ready(function(){
//==============================================================================

/*==============================================================================
  Send ajax to server
==============================================================================*/

  // On page load : send ajax
  sendAjax("ajxPage.php", {});



  // Every 60s : send ajax
  window.setInterval(sendAjax, 60000, "ajxPage.php", {});



  // On keyup (login) : send ajax
  jQuery("body").on("keyup", "input[name='login']", function(key) {
    var login = jQuery(this).val();
    if (key.which == 13) alert("Vous avez appuyé sur ENTREE : login=" + login);
    sendAjax("ajxPage.php", {login: login});
  });





/*==============================================================================
  Receive ajax from server
==============================================================================*/

  // Receive ajax data
  function receiveAjax(data) {
    // TODO

    // On success : update html content
    if (data['success']) jQuery(".aClass").html(data['html']);
    // On fail : logout
    else redirect("logout.php");

    // Append content to <ul>
    for (var val of data['obj']) {
      jQuery("ul").append("<li>" + val + "</li>");
    }
  }



















/*==============================================================================
  Usefull functions
==============================================================================*/

  // --- Send AJAX data to server
  function sendAjax(serverUrl, data) {
    jsonData = JSON.stringify(data);
    jQuery.ajax({type: 'POST', url: serverUrl, dataType: 'json', data: "data=" + jsonData,
      success: function(data) {
        receiveAjax(data);
      }
    });
  }



  // --- Redirect
  function redirect(serverUrl) {
    window.location.href = serverUrl;
  }



  // --- Test whether a variable is defined or not
  function defined(myVar) {
    if (typeof myVar != 'undefined') return true;
    return false;
  }

//==============================================================================
});
