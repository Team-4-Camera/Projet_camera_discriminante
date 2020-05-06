<div id="contenu">
	<img src="image/camera.PNG">
	<p>
		L'ajout d'une nouvelle personne donne l'accès a cette dernière. La camera ne vous enverra pas de notifications lorsque la personne se trouve dans son champs de surveillance
	</p>	
	<form method="POST" action="index.php?uc=personne&action=addPerson">
		<input type="submit" value="Ajouter une nouvelle personne" name="add">
	</form>

	<form method="POST" action="index.php?uc=notification&action=vueNotif">
		<input type="submit" value="Voir les notifications" name="notif">
	</form>
</div>