<?php
if (! isset ( $_REQUEST ['action'] )) {
	$_REQUEST ['action'] = 'premierepage';
}
$action = $_REQUEST ['action'];
switch ($action) {
	case 'premierepage' :
		{
			include ("vue/v_acceuil.php");
			break;
		}
	}
?>