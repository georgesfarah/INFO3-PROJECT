<?php

$username=$_POST["username"];
$password=$_POST["password"];

$adminuser="b'\\x9ar\\x03\\xf0 6`\\x17\\xd8\\x1ek\\xc7\\x179\\xa7\\x12#_\\xf0\\x1a/\\xc8\\xd3@\\xbfw\\xf5\\xfc\\xb1Eo\\xe5'";
$adminpass="b'\\xa1\\xbat\\xc6\\xd7\\xcez\\xb1O<BEw\\x02\\xac\\x1aOk.\\x7fD\\x0b\\xff\\x9cYa\\xf7.\\xba\\xcbZ\\x8f'";

if($username==$adminuser && $password==$adminpass){
$file = file_get_contents( 'data.txt' );
$array1= json_decode( $file );

$userpass=array('user'=>'johndoe@gmail.com','pass'=>'password123');

echo json_encode(array("feedbacks" =>$array1,"userpass" =>$userpass));

}
else{
  echo json_encode(array());
}
?>
