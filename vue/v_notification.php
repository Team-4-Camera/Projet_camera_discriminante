
<div>

	<h2>Recherche</h2>
<form action="index.php?uc=notification&action=vueNotif" method="post" enctype="multipart/form-data">
<label for="selectType">choisir un type:</label>

<select name="affiche" id="affiche-select">
	<?php
	foreach ($listType as $key => $value) { 
   ?> <option value="<?php echo $key ?>"><?php echo $value ?></option><?php 

	}

	?>
</select>

<label for="selectDate">choisir une date:</label>

<select name="date" id="date-select">
<?php
	foreach ($listDate as $key => $value) { 
   ?> <option value="<?php echo $key ?>"><?php echo $value ?></option><?php 

	}

	?>
</select>

 <input type="submit" name="valider" id="valider" value="Valider" />
</form>
<?php
if(sizeof($lesDossiers) > 0) {?>

	<h2>Les animaux</h2>
	<?php

 	afficheImage($lesDossiers,"./animaux/",0);
}
if(sizeof($lesPersonnes) > 0) {?>
	<h2>Les personnes</h2>
	<?php
 afficheImage($lesPersonnes,"./humains/",0);
}

if ( sizeof($lesDossiers) == 0 and sizeof($lesPersonnes) == 0){
	?>
<p>
	Aucun éléments ne corresponds à vos critères de recherche
</p>
	<?php
}
?>


</div>