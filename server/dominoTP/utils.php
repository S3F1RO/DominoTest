<?php
////////////////////////////////////////////////////////////////////////////////
// Utils library
////////////////////////////////////////////////////////////////////////////////



  // Generate random string
  function generateRandomString($length=100) {
    $characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    $randomString = '';
    for ($i = 0 ; $i < $length ; $i++) {
      $randomString .= $characters[rand(0, strlen($characters) - 1)];
    }
    return $randomString;
  }



  // SUCCESS / FAIL functions
  function success($db=NULL, $result=NULL, $html=NULL, $obj=NULL, $fields=[]) {
    // DB close
    if ($db != NULL) $db->close();

    // Result close
    if ($result != NULL) $result->close();

    // Merge
    $out = array_merge(["success"=>true, "html"=>$html, "obj"=>$obj], $fields);

    // Data ajax to client
    echo json_encode($out);
    exit();
  }
  function fail($db=NULL, $result=NULL, $errorMsg=NULL) {
    // DB close
    if ($db != NULL) $db->close();

    // Result close
    if ($result != NULL) $result->close();

    // Data ajax to client
    echo json_encode(array("success"=>false, "errorMsg"=>$errorMsg));
    exit();
  }
  function logout($db=NULL, $result=NULL) {
    // DB close
    if ($db != NULL) $db->close();

    // Result close
    if ($result != NULL) $result->close();

    // Logout
    header("Location: logout.php");
    exit();
  }
  function redirect($page, $db=NULL, $result=NULL) {
    // DB close
    if ($db != NULL) $db->close();

    // Result close
    if ($result != NULL) $result->close();

    // Logout
    header("Location: $page");
    exit();
  }

?>
