<?php
if (! isset ( $_REQUEST ['action'] )) {
	$_REQUEST ['action'] = 'vueNotif';
}
$action = $_REQUEST ['action'];
switch ($action) {
	case 'vueNotif' :
		{
            //explore le dossier des animaux et le retourne sous forme de tableau
			$lesDossiers = explorer("./animaux");
             //explore le dossier des humains et le retourne sous forme de tableau
			$lesPersonnes = explorer("./humains");
            // creer une liste de toutes les dates selectionnable
			$listDate = listDate($lesDossiers, $lesPersonnes);
              // creer une liste de toutes les types selectionnable
			$listType = listType($lesDossiers);
			
             // Si une recherche a été effectuté
			if (isset($_POST['affiche'])){
				switch ($_POST['affiche']) {
    				case "All":
                         // on ne fait rien
        				 break;
    			     case "animaux":
                         // on vide le tableau
        			     $lesPersonnes= array();
        			     break;
    			     case "personnes":
                        // on vide le tableau
        			     $lesDossiers = array();
        			     break;
    			     default:
                        // on applique une restiction sur le type d'animaux
    				    $lesDossiers = restrictionType($lesDossiers, $_POST['affiche']);
    	 			    $lesPersonnes = array();
				}
        	}
            // Si une recherche a été effectuté
        	if (isset($_POST['date'])){
        		if ($_POST['date'] != "All"){
                    if(!is_null($lesPersonnes)){
                        // on applique une restiction sur les personnes par date
                        $lesPersonnes = restrictionDate($lesPersonnes, $_POST['date'], true);
                    }
        			 if(!is_null($lesDossiers)){
                        // on applique une restiction sur les animaux par date
        			     $lesDossiers = restrictionDate($lesDossiers, $_POST['date'], false);
                    }
        		}
        	}

			include ("vue/v_notification.php");
			break;
		}
	}
?>