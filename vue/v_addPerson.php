<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.0/jquery.min.js"></script>
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css" />
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
<script src="./styles/js/scripts.js"></script>

<!-- Partie Tableau des dossiers -->

<body>
  <br /><br />
  <div class="container">
    <h2 align="center">Création de dossiers</a></h2>
    <br />
    <div align="right">
      <button type="button" name="create_folder" id="create_folder" class="btn btn-success">Nouveau dossier</button>
    </div>
    <br />
    <div class="table-responsive" id="folder_table">

    </div>


    <!-- Demarrage de carméra -->
    <div>
      <div class="button-group">
        <button id="btn-start" type="button" class="btn btn-info">Demarer</button>
        <button id="btn-stop" type="button" class="btn btn-danger">Arreter</button>
        <button id="btn-capture" type="button" class="btn btn-success">Capture Image</button>

      </div>
    </div>

    <!-- Video Element & Canvas -->
    <div class="play-area">
      <div class="play-area-sub">
        <h3>Enregistrement</h3>
        <video id="stream" width="320" height="240"></video>
      </div>
      <div class="play-area-sub">
        <h3>La Capture</h3>
        <canvas id="capture" width="320" height="240"></canvas>
        <div id="snapshot"></div>
      </div>
    </div>
  </div>



  </div>
</body>

<!-- boite de dialogue -->
<div id="folderModal" class="modal fade" role="dialog">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal">&times;</button>
        <h4 class="modal-title"><span id="change_title">Création de dossier</span></h4>
      </div>
      <div class="modal-body">
        <p>Entrer le nom du dossier
          <input type="text" name="folder_name" id="folder_name" class="form-control" /></p>
        <br />
        <input type="hidden" name="action" id="action" />
        <input type="hidden" name="old_name" id="old_name" />
        <input type="button" name="folder_button" id="folder_button" class="btn btn-info" value="Créer" />

      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-default" data-dismiss="modal">Fermer</button>
      </div>
    </div>
  </div>
</div>

<script src="./styles/js/camera.js"></script>