<?php
if (! isset ( $_REQUEST ['action'] )) {
	$_REQUEST ['action'] = 'vueNotif';
}
$action = $_REQUEST ['action'];
switch ($action) {
	case 'vueNotif' :
		{
			$lesDossiers = explorer("./animaux");
			$lesPersonnes = explorer("./humains");
			include ("vue/v_notification.php");
			break;
		}
	}
?>