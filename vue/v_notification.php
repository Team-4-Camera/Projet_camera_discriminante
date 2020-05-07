
<div>





<?php





function test_print($item, $key)
{
    echo "La clé $key contient l'élément $item\n";
    if( is_array($item)){
    	    //array_walk_recursive($item, 'test_print');
    }

}

array_walk_recursive($lesDossiers, 'test_print');


//	foreach ($lesDossiers as $ledossier => $lesFichiers) {
 //var_dump($ledossier);
?>

	
<?php

//<img src= "<?php echo $ledossier"  alt="chien"  height="150" width="150"/>
?>

</div>