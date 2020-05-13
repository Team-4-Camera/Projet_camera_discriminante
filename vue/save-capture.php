<?php
$image = $_POST["image"];
$str = rand();
$image = explode(";", $image)[1];
$image = explode(",", $image)[1];
$image =str_replace(" ", "+", $image);
$image = base64_decode($image);

file_put_contents("../humains/".$str."p.png", $image);
echo "Done";

