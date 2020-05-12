<?php
if (! isset ( $_REQUEST ['action'] )) {
    $_REQUEST ['action'] = 'addPerson';
}
$action = $_REQUEST ['action'];
switch ($action) {
    case 'addPerson' :
        {
            $directory = createDirectory();
            include ("vue/v_addPerson.php");
            break;
        }
    }
?>