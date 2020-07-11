<?php

$name=$_POST["name"];
$emailaddress=$_POST["emailaddress"];
$message=$_POST["message"];
$stars=$_POST["stars"];

$array1=array("name" => $name, "emailaddress" => $emailaddress, "message" => $message, "stars" => $stars);

$file = file_get_contents( 'data.txt' );

if(empty($file)){

  $array2=array($array1);
  file_put_contents( 'data.txt', json_encode( $array2 ) );
  echo 'done';

}
else{
  $array2 = json_decode( $file );
  array_push($array2,$array1);
  file_put_contents( 'data.txt', json_encode( $array2 ) );
  echo 'done';
}


?>
