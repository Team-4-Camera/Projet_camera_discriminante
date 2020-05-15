import os
import numpy as np
import tensorflow.compat.v1 as tf
import cv2
import time
import variables_algo as var_algo
import envoi_mail
#import envoi_sms

tf.disable_v2_behavior()

face_cascade = cv2.CascadeClassifier("./haarcascade_frontalface_alt2.xml")

labels = var_algo.labels
chemin_animaux = var_algo.chemin_animaux
switcher = var_algo.switcher
min_size = var_algo.min_size
modele_detection = var_algo.modele_detection
chemin_graphe = var_algo.chemin_graphe
dir_videos = var_algo.dir_videos
precision_retenue = var_algo.precision_retenue
fin_mouvement = var_algo.fin_mouvement
confirmation_detection = var_algo.confirmation_detection

fichier_video = None
fichier_photo = None
nom_video = ""
nom_photo = ""
cpt_fin_mouvement = -1
cpt_confirmation_detection = confirmation_detection
nb_objets_precedent = -1
nb_objets = 0
classes = []
boxes = []
scores = []

# Récupération du fichier d'entrainement
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("trainner.yml")
id_image = 0
color_infos = (255, 255, 255)
color_ko = (0, 0, 255)
color_ok = (0, 255, 0)

source_video = "video1.mp4"  # la source de la vidéo, 0 pour cam intégré (sys.argv[] cast en int si argument), nom d'un fichier pour vidéo
destinataire = "xxxxxx@xxx.x"  # l'adresse mail du destinataire à qui sera envoyé le mail


# *************************** Partie Fonctions *************************************

def recupererNbObjetsPersonneAnimaux(output_dict):
    nb_objets = 0
    for objet in range(int(output_dict['num_detections'])):  # on parcourt tous les objets détectés sur l'image
        local_classes = output_dict['detection_classes'][0].astype(np.uint8)  # le tableau avec les identifiants
        local_scores = output_dict['detection_scores'][0]  # indice de confiance renvoyé pour chaque objet
        if local_scores[objet] > precision_retenue \
                and local_classes[objet] in {1, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25}:
            nb_objets = nb_objets + 1

    return nb_objets


# *************************** Partie IA tensorflow *************************************

# lecture du modèle qui a déjà été entrainée avec le dataset COCO
detection_graph = tf.Graph()
with detection_graph.as_default():
    od_graph_def = tf.GraphDef()
    # recupère le modèle
    with tf.gfile.GFile(chemin_graphe, 'rb') as fid:
        serialized_graph = fid.read()
        od_graph_def.ParseFromString(serialized_graph)
        # importe od_graph_def dans le graph courant
        tf.import_graph_def(od_graph_def, name='')

with detection_graph.as_default():
    with tf.Session() as sess:
        cap = cv2.VideoCapture(source_video)  # récupére les images de la source
        ops = tf.get_default_graph().get_operations()  # retourne la liste des opérations dans le graphe
        all_tensor_names = {output.name for op in ops for output in op.outputs}
        tensor_dict = {}
        for key in [
            'num_detections', 'detection_boxes', 'detection_scores',
            'detection_classes', 'detection_masks']:
            tensor_name = key + ':0'
            if tensor_name in all_tensor_names:
                tensor_dict[key] = tf.get_default_graph().get_tensor_by_name(tensor_name)
        if 'detection_masks' in tensor_dict:
            quit("Masque non géré")
        image_tensor = tf.get_default_graph().get_tensor_by_name('image_tensor:0')

        # ************************* Partie exploitation de la vidéo ***********************************

        while True:
            ret, frame = cap.read()  # lit les images provenant de la source vidéo
            hauteur, largeur, nbr_couche = frame.shape
            output_dict = sess.run(tensor_dict, feed_dict={
                image_tensor: np.expand_dims(frame, 0)})  # donne notre image au réseau de neurones

            # récupére le nombre d'objets personne et animaux présents sur la frame
            nb_objets_personne_animaux = recupererNbObjetsPersonneAnimaux(output_dict)

            # on décremente le compteur si on constate le même nombre d'objets en n et n-1 et qu'il est supérieur à 0
            if nb_objets_personne_animaux == nb_objets_precedent:
                if cpt_confirmation_detection > 0:
                    cpt_confirmation_detection = cpt_confirmation_detection - 1
            # sinon on réinitialise le compteur si on constate une différence de nombre d'objets
            else:
                cpt_confirmation_detection = confirmation_detection
                nb_objets_precedent = nb_objets_personne_animaux

            # si le compteur est égal à 0, on met à jour les objets présents sur la frame
            if cpt_confirmation_detection == 0:
                nb_objets = int(output_dict['num_detections'])  # nombre d'objets présents
                classes = output_dict['detection_classes'][0].astype(np.uint8)  # le tableau avec les identifiants
                boxes = output_dict['detection_boxes'][0]  # les coordonnées localisant les objets
                scores = output_dict['detection_scores'][0]  # indice de confiance renvoyé pour chaque objet

            for objet in range(nb_objets):  # on parcourt tous les objets détectés sur l'image

                ymin, xmin, ymax, xmax = boxes[objet]

                # si le score est supérieur au paramétrage
                if scores[objet] > precision_retenue:
                    if classes[objet] in {1, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25}:
                        # TODO: supprimer les lignes suivantes qui ne nous servent que pour les tests
                        height, width = frame.shape[:2]
                        xmin = int(xmin * width)
                        xmax = int(xmax * width)
                        ymin = int(ymin * height)
                        ymax = int(ymax * height)
                        cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), color_infos, 1)
                        txt = "{:s}:{:3.0%}".format(labels[classes[objet]], scores[objet])
                        cv2.putText(frame, txt, (xmin, ymin - 5), cv2.FONT_HERSHEY_PLAIN, 1, color_infos, 2)

                    # S'il s'agit d'une personne
                    if classes[objet] == 1:

                        # TODO: Timer de x secondes avant d'envoyer une notif ici
                        tickmark = cv2.getTickCount()
                        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                        # détecte des objets de différentes tailles dans l'image d'entrée.
                        # les objets détectés sont renvoyés sous forme de liste de rectangles.
                        face = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=4,
                                                             minSize=(min_size, min_size))
                        for x, y, w, h in face:
                            # Si le visage est compris dans la zone de détection de la personne
                            if x >= xmin and x + w <= xmax and y >= ymin and y + h <= ymax:
                                # TODO: Dans le if ou le else (connu ou non sur la frame) mettre la condition de notif
                                # à étaler sur plusieurs frames pour être sûr ? En discussion
                                roi_gray = cv2.resize(gray[y:y + h, x:x + w], (var_algo.min_size, var_algo.min_size))
                                id_, conf = recognizer.predict(roi_gray)
                                # TODO: supprimer les couleurs & labels qui ne servent que pour nos tests
                                if conf <= 95:
                                    color = color_ok
                                    name = labels[id_]
                                else:
                                    color = color_ko
                                    name = "Inconnu"
                                    fichier_photo = None
                                    nom_photo = ""
                                label = name + " " + '{:5.2f}'.format(conf)
                                cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_DUPLEX, 1, color_infos, 1,
                                            cv2.LINE_AA)
                                # TODO: supprimer la création des rectangles qui ne sert que pour nos tests
                                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

                    if classes[objet] in {16, 17, 18, 19, 20, 21, 22, 23, 24, 25}:  # si un animal est détecté
                        # Une hashmap par quadruplet de coordonnées dont la distance avec la frame n+1 est comparée avec celle des autres
                        # coordonnées des hashmap du même type d'objet
                        # Exemple de la Hashmap : {1 => {(2, 5, 14, 19) => 40, (50,59,62,72) => 35}, 16 =>}
                        # {"person" => {(xmin1, xmax1, ymin1, ymax1) => cpt1, (xmin2, xmax2, ymin2, ymax2) => cpt2},
                        # "cat" => {(xmin3, xmax3, ymin3, ymax3) => cpt3}}

                        # récupére le répertoire concernant l'animal détecté
                        dir_photos = chemin_animaux + switcher.get(classes[objet]) + "/"

                        # crée le repertoire du jour courant s'il n'existe pas
                        if not os.path.isdir(dir_photos + time.strftime("%Y_%m_%d")):
                            os.mkdir(dir_photos + time.strftime("%Y_%m_%d"))

                        # met à jour le répertoire ou il faut enregistrer l'image de l'animal
                        dir_photos = dir_photos + time.strftime("%Y_%m_%d") + "/"

                        # on crée un fichier photo
                        if fichier_photo is None:
                            nom_photo = time.strftime("%Y_%m_%d_%H_%M_%S") + ".png"
                            fichier_photo = dir_photos + nom_photo
                            cv2.imwrite(fichier_photo, frame)

                        cpt_fin_mouvement = fin_mouvement  # on initialise ou réinitialise le compteur

                        # on crée un fichier video s'il s'agit de la premiere image enregistrée
                        # if fichier_video is None:
                        #    nom_fichier = time.strftime("%Y_%m_%d_%H_%M_%S") + ".avi"
                        #    fichier_video = dir_videos + nom_fichier
                        #    video = cv2.VideoWriter(fichier_video, cv2.VideoWriter_fourcc(*'DIVX'), 15,
                        #                            (largeur, hauteur))

                        # cpt_fin_mouvement = fin_mouvement  # on initialise ou réinitialise le compteur

            # if cpt_fin_mouvement > 0:
            #     video.write(frame)  # on écrit dans la video tant que le compteur n'atteint pas 0

            # si l'animal n'a pas été détecté depuis cpt_fin_mouvement frame, on envoie un mail et on réinitialise
            if cpt_fin_mouvement == 0:
                envoimail.envoyermail(destinataire, "Détection animal", "Un animal sauvage a été détecté",
                                      dir_photos, nom_photo)
                fichier_photo = None
                nom_photo = ""

            cpt_fin_mouvement = cpt_fin_mouvement - 1

            # if cpt_fin_mouvement == 0:
            #     envoimail.envoyermail(destinataire, "Intrusion",
            #                           "Un pangolin sauvage a été détecté", dir_videos, nom_fichier)
            #     video.release()  # on cloture la video si aucun animal n'a été détecté depuis cpt_fin_mouvement images
            #     fichier_video = None
            #     nom_fichier = ""

            # cpt_fin_mouvement = cpt_fin_mouvement - 1

            # TODO: supprimer l'affichage de la fenetre qui ne nous sert que pour les tests
            cv2.imshow('image', frame)

            # TODO: supprimer la gestion des keys qui ne nous sert que pour les tests
            key = cv2.waitKey(1) & 0xFF
            if key == ord('a'):
                for objet in range(500):
                    ret, frame = cap.read()
            if key == ord('q'):
                break

        cap.release()
        # TODO: supprimer la destruction de fenetre qui ne nous sert que pour les tests
        cv2.destroyAllWindows()
