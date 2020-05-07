<SCRIPT LANGUAGE="JAVASCRIPT" TYPE="text/javascript">

</script> 
<?php 

function explorerIterator($chemin){  

 $files = array();
$it = new RecursiveIteratorIterator(new RecursiveDirectoryIterator($chemin));
 
while($it->valid()) {
	if (!$it->isDot()) {
		//echo 'SubPathName: ' . $it->getSubPathName() . "\n";
		//echo 'SubPath:	 ' . $it->getSubPath() . "\n";
		//echo 'Key:		 ' . $it->key() . "\n\n";

		array_push($files ,$it->key()); 
	}
 
	$it->next();
}

return $files;
}



function explorer($chemin){  
    // Si $chemin est un dossier on le parcours
    if( is_dir($chemin) ){
        $me = opendir($chemin);
        while( $child = readdir($me) ){
            if( $child != '.' && $child != '..' ){
                explorer( $chemin.DIRECTORY_SEPARATOR.$child );
            }
        }
    }else{
    	    echo "$chemin   type: $filetype size: $lstat[size]  mtime: $mtime\n";
    }
}


?>
