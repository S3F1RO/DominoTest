<?php

  // Session open
  session_start();

  // Destroy session cookie
  $sessionCookie = session_get_cookie_params();
  setcookie(session_name(), '', time() - 1, $sessionCookie["path"], $sessionCookie["domain"], $sessionCookie["secure"], $sessionCookie["httponly"]);

  // Unset session vars
  session_unset();

  // Session close, go to index page
  if (session_destroy()) {
    header("Location: index.php");
  }
  
?>
