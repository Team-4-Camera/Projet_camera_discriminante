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
				<img src= "<?php echo  $chemin.$value?>"  alt="<?php echo $chemin.$value ?>"  height="300" width="300"/><?php
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

?>
