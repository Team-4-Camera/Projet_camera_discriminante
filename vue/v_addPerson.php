<form action="index.php?uc=personne&action=addPerson" method="post" enctype="multipart/form-data" name="form1" id="form1">
  <p>
    <label for="directory">Nouveau dossier:</label>
    <input value="<?php if ($_POST) {
                    echo htmlentities($_POST['directory'], ENT_COMPAT, 'UTF-8');
                  } ?>" type="text" name="directory" id="directory" />
  </p>
  <p>
    <input type="submit" name="insert" id="insert" value="Valider" />
  </p>
</form>

<div>
  <div class="button-group">
    <button id="btn-start" type="button" class="button">Demarer</button>
    <button id="btn-stop" type="button" class="button">Arreter</button>
    <button id="btn-capture" type="button" class="button">Capture Image</button>

  </div>
  <div>


  </div>
  <!-- Video Element & Canvas -->
  <div class="play-area">
    <div class="play-area-sub">
      <h3>The Stream</h3>
      <video id="stream" width="320" height="240"></video>
    </div>
    <div class="play-area-sub">
      <h3>The Capture</h3>
      <canvas id="capture" width="320" height="240"></canvas>
      <div id="snapshot"></div>
    </div>
  </div>
</div>
<script src="./styles/js/camera.js"></script>