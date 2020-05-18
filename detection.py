import os
import numpy as np
import tensorflow.compat.v1 as tf
import cv2
import time
import variables_algo as var_algo
import envoi_mail
import logging

# import envoi_sms

# TODO: supprimer le log
logging.basicConfig(filename='test_log.log',level=logging.DEBUG,\
      format='%(asctime)s -- %(name)s -- %(levelname)s -- %(message)s')


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

source_video = "test1.mp4"  # la source de la vidéo, 0 pour cam intégré (sys.argv[] cast en int si argument), nom d'un fichier pour vidéo
destinataire = "robin.lemancel@gmail.com"  # l'adresse mail du destinataire à qui sera envoyé le mail

classes_hashmap = {1: {}, 16: {}, 17: {}, 18: {}, 19: {},
                       20: {}, 21: {}, 22: {}, 23: {}, 24: {}, 25: {}}


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


def majClassesHashmap(output_dict):

    coord_hashmap = {1: [], 16: [], 17: [], 18: [], 19: [],
                       20: [], 21: [], 22: [], 23: [], 24: [], 25: []}

    for objet in range(int(output_dict['num_detections'])):  # on parcourt tous les objets détectés sur l'image

        local_classes = output_dict['detection_classes'][0].astype(np.uint8)  # le tableau avec les identifiants
        local_boxes = output_dict['detection_boxes'][0]  # les coordonnées localisant les objets
        local_scores = output_dict['detection_scores'][0]  # indice de confiance renvoyé pour chaque objet

        if local_classes[objet] in {1, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25} and local_scores[objet] > precision_retenue:

            classes_id = local_classes[objet]
            tmp_ymin, tmp_xmin, tmp_ymax, tmp_xmax = local_boxes[objet]
            tmp_coord = (tmp_xmin, tmp_xmax, tmp_ymin, tmp_ymax)
            coord_hashmap[classes_id].append(tmp_coord)

    for id_classes, coord_liste in coord_hashmap.items():
        majValeurHashmap(id_classes, coord_liste)


def majValeurHashmap(id_classes, coord_liste):
    tmp_hashmap = {}
    value_hashmap = classes_hashmap[id_classes]
    new_value_hashmap = {}

    i = 0

    for key_value_hashmap, value_value_hashmap in value_hashmap.items():
        tmp_coord = value_value_hashmap[0]

        for coord in coord_liste:
            comp_xmin = abs(tmp_coord[0] - coord[0])
            comp_xmax = abs(tmp_coord[1] - coord[1])
            comp_ymin = abs(tmp_coord[2] - coord[2])
            comp_ymax = abs(tmp_coord[3] - coord[3])
            indicateur_confiance = comp_xmin + comp_xmax + comp_ymin + comp_ymax
            tmp_hashmap[i] = (coord, indicateur_confiance)
            i = i + 1

        indicateur_confiance = 999999
        coord_plus_proches = None
        for key_tmp_hashmap, value_tmp_hashmap in tmp_hashmap.items():
            if value_tmp_hashmap[1] < indicateur_confiance:
                coord_plus_proches = value_tmp_hashmap[0]

        if coord_plus_proches in coord_liste:
            coord_liste.remove(coord_plus_proches)
            new_value_hashmap[key_value_hashmap] = [coord_plus_proches, value_hashmap[key_value_hashmap][1],
                                                    value_hashmap[key_value_hashmap][2]]
        elif value_hashmap[key_value_hashmap][1] >= 0:
            new_value_hashmap[key_value_hashmap] = value_hashmap[key_value_hashmap]

    value_hashmap = new_value_hashmap

    if len(coord_liste) > 0:
        for coord in coord_liste:
            id_disponible = hashmapIdDisponible(value_hashmap)
            value_hashmap[id_disponible] = [coord, fin_mouvement, None]

    classes_hashmap[id_classes] = value_hashmap



def hashmapIdDisponible(hashmap):
    id_disponible = -1
    if len(hashmap) == 0:
        id_disponible = 0
    for i in range(1000):
        for key, value in hashmap.items():
            if key == i:
                break
            id_disponible = i
        if id_disponible != -1:
            break

    return id_disponible


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
                majClassesHashmap(output_dict)

            for objet in range(nb_objets):  # on parcourt tous les objets détectés sur l'image

                ymin, xmin, ymax, xmax = boxes[objet]

                # si le score est supérieur au paramétrage
                if scores[objet] > precision_retenue:
                    if classes[objet] in {1, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25}:

                        # TODO: supprimer les lignes suivantes qui ne nous servent que pour les tests
                        ymin, xmin, ymax, xmax = boxes[objet]
                        coord = (xmin, xmax, ymin, ymax)
                        for key, value in classes_hashmap[classes[objet]].items():
                            if value[0] == coord:
                                id_objet = key
                                cpt_fin_mouvement = value[1]
                                fichier_photo = value[2]

                        if fichier_video != None:
                            color_infos = color_ko
                        else:
                            color_infos = color_ok

                        height, width = frame.shape[:2]
                        xmin = int(xmin * width)
                        xmax = int(xmax * width)
                        ymin = int(ymin * height)
                        ymax = int(ymax * height)
                        cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), color_infos, 1)
                        txt = "{:s}:{:3.0%}".format(labels[classes[objet]] + " cpt = " + str(cpt_fin_mouvement), scores[objet])
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

                        ymin, xmin, ymax, xmax = boxes[objet]
                        coord = (xmin, xmax, ymin, ymax)

                        for key, value in classes_hashmap[classes[objet]].items():
                            if value[0] == coord:
                                id_objet = key
                                cpt_fin_mouvement = value[1]
                                fichier_photo = value[2]

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
                            classes_hashmap[classes[objet]][id_objet][2] = fichier_photo
                            cv2.imwrite(fichier_photo, frame)

                        classes_hashmap[classes[objet]][id_objet][1] = fin_mouvement  # on initialise ou réinitialise le compteur

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
            for key, value in classes_hashmap.items():
                if key in {16, 17, 18, 19, 20, 21, 22, 23, 24, 25}:
                    for key2, value2 in classes_hashmap[key].items():
                        if value2[1] == 0:  # cpt_fin_mouvement
                            nom_photo = value2[2].split("/")[-1]
                            dir_photos = value2[2].replace(nom_photo, "")
                            envoi_mail.envoyermail(destinataire, "Détection animal", "Un animal sauvage a été détecté",
                                                   dir_photos, nom_photo)
                            value2[2] = None

                        logging.debug(classes_hashmap)
                        value2[1] = value2[1] - 1

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
