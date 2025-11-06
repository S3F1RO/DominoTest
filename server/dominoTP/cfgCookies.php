<?php

  // Session cookie parameters
  session_name('CUSTOM_SESSID');     // Custom name
  session_set_cookie_params([
    'lifetime' => 3600,              // Cookie expiration time
    'path'     => '/',               // Available across the entire domain
    'domain'   => '',                // Current domain (leave empty for security)
    'secure'   => true,              // Only send cookie over HTTPS
    'httponly' => true,              // Prevent JavaScript access (security)
    'samesite' => 'Strict'           // Mitigate CSRF attacks
  ]);

  // Cookie parameters
  define("COOKIE_LIFETIME", 3600);
  define("COOKIE_PATH", "/");
  define("COOKIE_DOMAIN", "");
  
?>
