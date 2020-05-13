<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
       "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="fr" lang="fr">
<head>
<title>Groupe 4 - Caméra discirminante</title>

<meta http-equiv="content-type" content="text/html; charset=utf-8" />
<link href="./styles/styles.css" rel="stylesheet" type="text/css" />
<meta name="viewport" content="width=device-width, initial-scale=1">
 <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">
 <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
 <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js"></script>
 <link href="styles/css/styles.css" rel="stylesheet" type="text/css" />
 
 </head>
<body>
	<div id="page">
	<!-- nav bar fixe -->
<nav class="navbar navbar-default">
  <div class="container-fluid">
    <!-- Collect the nav links, forms, and other content for toggling -->
    <div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
      <ul class="nav navbar-nav">
        <li><a class="glyphicon glyphicon-home" href="index.php?uc=acceuil"  > ACCEUIL</a></li>
		<li class="dropdown">
          <a  class="glyphicon glyphicon-user"  href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false"> OPTIONS <span class="caret"></span></a>
          <ul class="dropdown-menu">
            <li><a href="index.php?uc=personne&action=addPerson">Ajouter une nouvelle personne</a></li>
            <li><a href="index.php?uc=notification&action=vueNotif">Voir les notifications</a></li>
          </ul>
        </li>
        <li><a class="glyphicon glyphicon-question-sign" href="#" Onclick="window.open(this.href, 'popup', 'height=350, width=700, toolbar=no, menubar=no, location=no resizable=yes, scrollbars=no, status=no'); return false;">
            AIDE EN LIGNE</a>
        </li>
        <li><a class="glyphicon glyphicon-arrow-left" href="javascript:history.back()"> RETOUR</a></li>
      </ul>

      <ul class="nav navbar-nav navbar-right">
	  <li class="nav-item dropdown no-arrow mx-1">
          <a class="nav-link dropdown-toggle" href="#" id="alertsDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
           <i class="fas fa-bell fa-fw"></i>
                <!-- Counter - Alerts -->
                <span class="badge badge-danger badge-counter">3+</span>
              </a>
              <!-- Dropdown - Alerts -->
              <div class="dropdown-list dropdown-menu dropdown-menu-right shadow animated--grow-in" aria-labelledby="alertsDropdown">
                <h6 class="dropdown-header">
                  Alerts Center
                </h6>
                <a class="dropdown-item d-flex align-items-center" href="#">
                  <div class="mr-3">
                    <div class="icon-circle bg-primary">
                      <i class="fas fa-file-alt text-white"></i>
                    </div>
                  </div>
                  <div>
                    <div class="small text-gray-500">December 12, 2019</div>
                    <span class="font-weight-bold">A new monthly report is ready to download!</span>
                  </div>
                </a>
                <a class="dropdown-item d-flex align-items-center" href="#">
                  <div class="mr-3">
                    <div class="icon-circle bg-success">
                      <i class="fas fa-donate text-white"></i>
                    </div>
                  </div>
                  <div>
                    <div class="small text-gray-500">December 7, 2019</div>
                    $290.29 has been deposited into your account!
                  </div>
                </a>
                <a class="dropdown-item d-flex align-items-center" href="#">
                  <div class="mr-3">
                    <div class="icon-circle bg-warning">
                      <i class="fas fa-exclamation-triangle text-white"></i>
                    </div>
                  </div>
                  <div>
                    <div class="small text-gray-500">December 2, 2019</div>
                    Spending Alert: We've noticed unusually high spending for your account.
                  </div>
                </a>
              </div>
        </li>
        <li class="dropdown">
          <a  class="glyphicon glyphicon-user"  href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false"> PROFIL <span class="caret"></span></a>
          <ul class="dropdown-menu">
            <li><a href="#">Préférences</a></li>
            <li><a href="#">Se déconnecter</a></li>
          </ul>
        </li>
      </ul>
    </div><!-- /.navbar-collapse -->
  </div><!-- /.container-fluid -->
</nav>
<!-- nav fin -->
<div id="entete">
	 <h1>Caméra Disciminante</h1>
</div>