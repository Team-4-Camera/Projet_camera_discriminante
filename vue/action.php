<?php
if(isset($_POST["action"]))
{
 if($_POST["action"] == "fetch")
 {
  $folder = array_filter(glob('../humains/*'), 'is_dir');
  
  $output = '
  <table class="table table-bordered table-striped">
   <tr>
    <th>Nom de dossier</th>
    <th>Modification</th>
    <th>Suppression</th>
   </tr>
   ';
  if(count($folder) > 0)
  {
   foreach($folder as $name)
   {
    $output .= '
     <tr>
      <td>'.$name.'</td>
      <td><button type="button" name="update" data-name="'.$name.'" class="update btn btn-warning btn-xs">Modifier</button></td>
      <td><button type="button" name="delete" data-name="'.$name.'" class="delete btn btn-danger btn-xs">Supprimer</button></td>
     </tr>';
   }
  }
  else
  {
   $output .= '
    <tr>
     <td colspan="6">Aucun dossier trouvé </td>
    </tr>
   ';
  }
  $output .= '</table>';
  echo $output;
 }
 
 // Création de dossier
 if($_POST["action"] == "create")
 {
  $dirname = $_POST["folder_name"];
  $filename = "../humains/" . $dirname . "/";
  if(!file_exists($filename)) 
  
  {
   mkdir("../humains/" . $dirname, 0777, true);
   echo 'Dossier crée';
  }
  else
  {
   echo 'Dossier existe déjà !';
  }
 }

 // Charger de dossier si possible 
 if($_POST["action"] == "change")
 {
  $dirname = $_POST["folder_name"];
  $oldDirname = $_POST["old_name"];
  $filename = "../humains/" . $dirname . "/";
  $oldFilename = "../humains/" . $oldDirname . "/";
  if(!file_exists($filename))
  {
   rename($oldFilename, $filename);
   echo 'Nom du dossier a été changé !';
  }
  else
  {
   echo 'Le dossier existe déjà !';
  }
 }
 
 if($_POST["action"] == "delete")
 {
  $dirname = $_POST["folder_name"];
  $filename = "../humains/" . $dirname . "/";
  $files = scandir($filename);
  foreach($files as $file)
  {
   if($file === '.' or $file === '..')
   {
    continue;
   }
   else
   {
    unlink($filename . '/' . $file);
   }
  }
  if(rmdir($filename))
  {
   echo 'Dossier supprimer';
  }
 }
 
 
}
