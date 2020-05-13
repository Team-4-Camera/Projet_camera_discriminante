$(document).ready(function(){
 
    load_folder_list();
    
    function load_folder_list()
    {
     var action = "fetch";
     $.ajax({
      url:"./vue/action.php",
      method:"POST",
      data:{action:action},
      success:function(data)
      {
       $('#folder_table').html(data);
      }
     });
    }
    
    $(document).on('click', '#create_folder', function(){
     $('#action').val("create");
     $('#folder_name').val('');
     $('#folder_button').val('Créer');
     $('#folderModal').modal('show');
     $('#old_name').val('');
     $('#change_title').text("Créer dossier");
    });
    
    $(document).on('click', '#folder_button', function(){
     var folder_name = $('#folder_name').val();
     var old_name = $('#old_name').val();
     var action = $('#action').val();
     if(folder_name != '')
     {
      $.ajax({
       url:"./vue/action.php",
       method:"POST",
       data:{folder_name:folder_name, old_name:old_name, action:action},
       success:function(data)
       {
        $('#folderModal').modal('hide');
        load_folder_list();
        alert(data);
       }
      });
     }
     else
     {
      alert("Enter Folder Name");
     }
    });
    
    $(document).on("click", ".update", function(){
     var folder_name = $(this).data("name");
     $('#old_name').val(folder_name);
     $('#folder_name').val(folder_name);
     $('#action').val("change");
     $('#folderModal').modal("show");
     $('#folder_button').val('Modifier');
     $('#change_title').text("Changer le nom du dossier");
    });
    
    $(document).on("click", ".delete", function(){
     var folder_name = $(this).data("name");
     var action = "delete";
     if(confirm("Êtes ous sûre de vouloir le supprimer ?"))
     {
      $.ajax({
       url:"./vue/action.php",
       method:"POST",
       data:{folder_name:folder_name, action:action},
       success:function(data)
       {
        load_folder_list();
        alert(data);
       }
      });
     }
    });  
   });
   