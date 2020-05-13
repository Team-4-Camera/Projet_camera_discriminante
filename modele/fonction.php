<SCRIPT LANGUAGE="JAVASCRIPT" TYPE="text/javascript">

</script> 
<?php 



function explorer($chemin){ 
$iterator = new RecursiveDirectoryIterator($chemin, RecursiveIteratorIterator::CHILD_FIRST);
$iterator->setFlags(RecursiveDirectoryIterator::SKIP_DOTS);
$ritit = new RecursiveIteratorIterator($iterator);
$r = array();
foreach ($ritit as $splFileInfo) {

   $path = $splFileInfo->isDir() 
         ? array($splFileInfo->getFilename() => array())
         : array($splFileInfo->getFilename());

   for ($depth = $ritit->getDepth() - 1; $depth >= 0; $depth--) {
       $path = array($ritit->getSubIterator($depth)->current()->getFilename() => $path);
   }

 
   $r = array_merge_recursive($r, $path);
}

return $r;
}


function afficheImage($lesDossiers, $chemin, $poid){
	foreach ($lesDossiers as $key => $value) {    
    	if (is_array($value)) {
    		if(preg_match("/[0-9]{4}_[0-9]{2}_[0-9]{2}/",$key)){
    			$titre = dateFormat($key);
    		}else{
				$titre = $key;
    		}
    		if ($poid == 0){
    			echo "<h3>".$titre."</h3>";
    		}
    		else{
				echo "<h4>".$titre."</h4>";
    		}      
        afficheImage($value, $chemin.$key."/",$poid+1 );
    	}else{
		 

     		if( strpos(mime_content_type($chemin.$value), 'video')  !== false){?>
				<video controls src="<?php echo  $chemin.$value?>" height="300" width="300" ><?php echo $chemin.$value ?></video><?php
     		}else{?>

				<a href="<?php echo  $chemin.$value?>" target="_blank"><img src= "<?php echo  $chemin.$value?>"  alt="<?php echo $chemin.$value ?>"  height="300" width="300" /></a>

				<!--<img src= "<?php //echo  $chemin.$value?>"  alt="<?php //echo $chemin.$value ?>"  height="300" width="300" onclick="window.open(this.src,'_blank',' width='+this.width+', height='+this.height);"/>--><?php
     		}
     		
     		
        }
	}
}


function dateFormat($date){

$newDate = explode("_", $date);

return $newDate[2]." ".searchMonth($newDate[1])." ".$newDate[0] ;
}


function searchMonth($month){

$string = array( "01" => "Janvier", 
				 "02" => "Février",
				 "03" => "Mars",
				 "04" => "Avril",
				 "05" => "Mai",
				 "06" => "Juin", 
				 "07" => "Juillet", 
				 "08" => "Août", 
				 "09" => "Septembre",
    			 "10" => "Octobre",
    			 "11" => "Novembre",
    			 "12" => "Décembre" );

return $string[$month]; 
}

function restrictionType($lesDossiers,$leType){
	foreach ($lesDossiers as $key => $value) { 
		if ($key != $leType){
			unset($lesDossiers[$key]); 
		}
	}

	return $lesDossiers;

}

function restrictionDate($lesDossiers,$laDate,$person){
	foreach ($lesDossiers as $key => $value) { 
		$supprimer = false;
		if ($key != $laDate and $person){
			$supprimer = true;
		}else{
			if(is_array($value)){
				foreach ($value as $k => $v) { 
					if ($k != $laDate){
						unset($lesDossiers[$key][$k]); 
						$supprimer = true;
					}
				}
			}
		}
		if($supprimer){
			if (empty($lesDossiers[$key])){
				unset($lesDossiers[$key]); 
			}
		}
	}

	return $lesDossiers;
}

function listType($lesDossiers){
	$my_array = array("All" => "Tout","animaux"=>"Les animaux","personnes" =>"Les personnes");
	foreach ($lesDossiers as $key => $value) {
	$my_array[$key] = "Les ".$key;
	}
	return $my_array;
}


function listDate($lesDossiers, $lesPersonnes){
	$my_array = array("All" => "Tout");
	foreach ($lesDossiers as $key => $value) {
		foreach ($value as $k => $v) { 
			if(preg_match("/[0-9]{4}_[0-9]{2}_[0-9]{2}/",$k)){
				$my_array[$k] = dateFormat($k);
			}else{
				$my_array[$k] = $k;
			}
		}
	}

	foreach ($lesPersonnes as $key => $value) {
		if(preg_match("/[0-9]{4}_[0-9]{2}_[0-9]{2}/",$key)){
			$my_array[$key] = dateFormat($key);
		}else{
			$my_array[$k] = $k;
		}
	}
	return $my_array;
}

?>
