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
    		if ($poid == 0){
    			echo "<h1>".$key."</h1>";
    		}
    		else{
				echo "<h3>".$key."</h3>";
    		}      
        afficheImage($value, $chemin.$key."/",$poid+1 );
    	}else{
     		?><img src= "<?php echo  $chemin.$value?>"  alt="chien"  height="150" width="150"/><?php
        }
	}
}

?>
