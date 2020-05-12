<?php
    function createDirectory(){
        try {
            if (isset($_POST['insert'])) {
                $directory = $_POST['directory'];
                $photo_destination = './image/';
                $path = $photo_destination;
                $new_path = $path . $directory;
                $mode = 0755;
                if(is_dir($new_path)) {
                    echo "The Directory {$directory} exists";
                    } else {
                        echo "The Directory {$new_path} was created";
                        init();
                        return mkdir($new_path , 0777);
                        }
                    }
            }catch (Exception $e) {
                echo 'Exception reçue : ',  $e->getMessage(), "\n";
            }
        } 
        function init(){
        $_GET['directory']='';
        }