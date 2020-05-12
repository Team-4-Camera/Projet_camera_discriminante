<?php
require_once("modele/fonction.php");
require_once("modele/fonction2.php");
include ("vue/v_header.php");
	if (! isset ( $_REQUEST ['uc'] )) {
		$_REQUEST ['uc'] = 'acceuil';
	}
	$uc = $_REQUEST ['uc'];
	switch ($uc) {
		case 'acceuil' :
			{
				include ("controleur/c_acceuil.php");
				break;
			}
		case 'personne' :
			{
				include ("controleur/c_person.php");
				break;
			}
		case 'notification' :
			{
				include ("controleur/c_notification.php");
				break;
			}
	}
include ("vue/v_footer.php");
?> 