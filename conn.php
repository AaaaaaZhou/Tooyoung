<?php
$host = "localhost";
$user = "root";
$pwd = "Zlx980616";
$dbname = "demo";

$link = mysqli_connect($host, $user, $pwd);
if(!$link) {
    exit("Failed in connection!");
}
mysqli_select_db($link, $dbname);
?>
