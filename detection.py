import os
import numpy as np
import tensorflow.compat.v1 as tf
import cv2
import time
import json
import variables_algo as var_algo
import envoi_mail
import envoi_sms
import Personne
import Animal
import re
from datetime import datetime, timedelta
import shutil

tf.disable_v2_behavior()

face_cascade = cv2.CascadeClassifier("./haarcascade_frontalface_alt2.xml")

id_animal = 91
chemin_animaux = var_algo.chemin_animaux
min_size = var_algo.min_size
modele_detection = var_algo.modele_detection
chemin_graphe = var_algo.chemin_graphe
chemin_humains = var_algo.chemin_humains
chemin_photos_temp = var_algo.chemin_photos_temp
precision_retenue = var_algo.precision_retenue
fin_mouvement = var_algo.fin_mouvement
longueur_video = var_algo.longueur_video
confirmation_detection = var_algo.confirmation_detection
coord_pourcentage = var_algo.coord_pourcentage
video_fps = var_algo.video_fps
chemin_gestion = var_algo.chemin_gestion
chemin_notifications_json = var_algo.chemin_notifications_json
chemin_enregistrements = var_algo.chemin_enregistrements

# Nombre de personnes inconnues et n'ayant pas encore déclenché l'alerte sur l'écran
cpt_personnes_inconnues = 0
# De 0 à 160, indique le numéro de la photo actuelle
cpt_photos_temp = 0
largeur = 0
hauteur = 0
etat_appli = "true"

# Récupération du fichier d'entrainement
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("..\\python\\trainner.yml")

# la source de la vidéo, 0 pour cam intégré (sys.argv[] cast en int si argument), nom d'un fichier pour vidéo
source_video = 0
date_courante = None
regex_date = re.compile("^([0-9]{4}(_[0-9]{2}){2})$")
classes_hashmap = {1: {}, 91: {}}

# *************************** Partie Fonctions *************************************


def majClassesHashmap(output_dict):
    """
    Stocke les coordonnées des objets détectés sur l'image
    Et lance le traitement pour mettre à jour la hashmap des objets
    Param : output_dict : le dictionaire généré de la détection des objets sur une image
    """

    coord_hashmap = {1: [], 91: []}

    # on parcourt tous les objets détectés sur l'image
    for objet in range(int(output_dict['num_detections'])):

        # le tableau avec les identifiants
        local_classes = output_dict['detection_classes'][0].astype(np.uint8)
        # les coordonnées localisant les objets
        local_boxes = output_dict['detection_boxes'][0]
        # indice de confiance renvoyé pour chaque objet
        local_scores = output_dict['detection_scores'][0]

        classes_id = local_classes[objet]
        # si l'objet est un animal, on attribue l'id animal général
        if local_classes[objet] in {16, 17, 18, 19, 20, 21, 22, 23, 24, 25}:
            classes_id = id_animal

        # si l'objet est détecté avec un bon indice de confiance
        if local_scores[objet] > precision_retenue and classes_id in {1, id_animal}:

            tmp_ymin, tmp_xmin, tmp_ymax, tmp_xmax = local_boxes[objet]
            tmp_coord = (tmp_xmin, tmp_xmax, tmp_ymin, tmp_ymax)
            # on fabrique pour chaque classe une liste des coordonnées détectées
            coord_hashmap[classes_id].append(tmp_coord)

    # on traite la liste de chaque classe pour mettre à jour le tableau des objets
    for id_classes, coord_liste in coord_hashmap.items():
        majValeurHashmap(id_classes, coord_liste)


def majValeurHashmap(id_classes, coord_liste):
    """
    Pour une classe donnée, compare les coordonnées stockées aux coordonnées détectées
    Pour mettre à jour, ajouter ou supprimer les objets de la hashmap objets
    Param : id_classes : l'id du type d'objet, 1 pour personne, 91 pour animal
            coord_liste : la liste des coordonnées détectées sur une image pour un type d'objet
    """

    value_hashmap = classes_hashmap[id_classes]
    new_value_hashmap = {}
    global cpt_personnes_inconnues

    i = 0

    # On parcourt les objets stockés pour la classe id_classes
    for key_value_hashmap, value_value_hashmap in value_hashmap.items():
        coord_initial = value_value_hashmap.get_coord()
        tmp_hashmap = {}

        # On parcourt toutes les coordonnées détectés pour cette classe
        for coord_coord_liste in coord_liste:
            comp_xmin = abs(coord_initial[0] - coord_coord_liste[0])
            comp_xmax = abs(coord_initial[1] - coord_coord_liste[1])
            comp_ymin = abs(coord_initial[2] - coord_coord_liste[2])
            comp_ymax = abs(coord_initial[3] - coord_coord_liste[3])
            # On calcule un indice pour savoir à quel point les coordonnées sont proches
            indicateur_confiance = comp_xmin + comp_xmax + comp_ymin + comp_ymax
            # On stocke les coordonnées avec l'indice
            tmp_hashmap[i] = (coord_coord_liste, indicateur_confiance)
            i = i + 1

        indicateur_confiance = 999999
        coord_plus_proches = None
        # On parcourt les coordonnées et les indices pour ressortir les coordonnées les plus proches
        for key_tmp_hashmap, value_tmp_hashmap in tmp_hashmap.items():
            if value_tmp_hashmap[1] < indicateur_confiance:
                coord_plus_proches = value_tmp_hashmap[0]
                indicateur_confiance = value_tmp_hashmap[1]

        objet_present = value_hashmap[key_value_hashmap]

        # Si on a trouvé des coordonnées
        # et qu'elles ne sont pas plus éloignées que d'un certain pourcentage des coordonnées initiales
        if coord_plus_proches is not None and coordAssezProches(coord_initial, coord_plus_proches):
            # On supprime de la liste des coordonnées détectées
            coord_liste.remove(coord_plus_proches)

            # On crée un nouvel objet contenant les propriétés de l'objet initial, en mettant à jour les coordonnées
            if id_classes == 1:
                new_value_hashmap[key_value_hashmap] = \
                    Personne.Personne(
                        coord_plus_proches,
                        fin_mouvement,
                        objet_present.get_chemin_fichier(),
                        objet_present.get_cpt_confirm_detection(),
                        objet_present.get_reconnu(),
                        objet_present.get_num_premiere_photo(),
                        objet_present.get_alerte_envoyee())

                if not objet_present.get_reconnu() \
                        and not objet_present.get_alerte_envoyee():
                    cpt_personnes_inconnues += 1
            else:
                new_value_hashmap[key_value_hashmap] = \
                    Animal.Animal(
                        coord_plus_proches,
                        fin_mouvement,
                        objet_present.get_chemin_fichier(),
                        objet_present.get_cpt_confirm_detection())

            objet_futur = new_value_hashmap[key_value_hashmap]
            # On diminue le compteur de la confirmation de détection à chaque frame jusqu'à 0
            if 0 < objet_futur.get_cpt_confirm_detection() <= confirmation_detection:
                objet_futur.set_cpt_confirm_detection(objet_futur.get_cpt_confirm_detection() - 1)

        # Si on a pas trouvé de coordonnées mais que le cpt fin mouvement est encore supérieur à 0
        # On garde l'objet dans le tableau
        elif objet_present.get_cpt_fin_mouvement() >= 0 and objet_present.get_cpt_confirm_detection() == 0:
                new_value_hashmap[key_value_hashmap] = objet_present

    # On met à jour le tableau des objets pour cette classe
    value_hashmap = new_value_hashmap

    # S'il reste des coordonnées qui n'ont pas été attribuées
    if len(coord_liste) > 0:
        for coord in coord_liste:
            id_disponible = hashmapIdDisponible(value_hashmap)
            # On crée un nouvel objet avec les coordonnées
            if id_classes == 1:
                value_hashmap[id_disponible] = \
                    Personne.Personne(coord, fin_mouvement, None, confirmation_detection, False, None, False)
            else:
                value_hashmap[id_disponible] = \
                    Animal.Animal(coord, fin_mouvement, None, confirmation_detection)

    # On met à jour la hashmap globale des objets détectés
    classes_hashmap[id_classes] = value_hashmap


def coordAssezProches(coord_initial, coord_plus_proches):
    """
    Compare deux ensembles de coordonnées
    Renvoie True si les deux ensembles sont proches de moins de coord_pourcentage
    Param : coord_initial : les coordonnées initiales de l'objet
            coord_plus_proches : les coordonnées à comparer
    """

    global hauteur, largeur

    pourcentage = coord_pourcentage / 100

    xmin_interval = (coord_initial[0] - pourcentage, coord_initial[0] + pourcentage)
    xmax_interval = (coord_initial[1] - pourcentage, coord_initial[1] + pourcentage)
    ymin_interval = (coord_initial[2] - pourcentage, coord_initial[2] + pourcentage)
    ymax_interval = (coord_initial[3] - pourcentage, coord_initial[3] + pourcentage)

    if coord_plus_proches[0] < xmin_interval[0] or coord_plus_proches[0] > xmin_interval[1]:
        return False
    if coord_plus_proches[1] < xmax_interval[0] or coord_plus_proches[1] > xmax_interval[1]:
        return False
    if coord_plus_proches[2] < ymin_interval[0] or coord_plus_proches[2] > ymin_interval[1]:
        return False
    if coord_plus_proches[3] < ymax_interval[0] or coord_plus_proches[3] > ymax_interval[1]:
        return False

    return True


def hashmapIdDisponible(hashmap):
    """
    Retourne un id disponible pour la hashmap passée en paramètre
    Permet de recycler les id au lieu de les incrémenter à l'infini
    Param : hashmap : un dictionnaire dans lequel on recherche un id disponible
    """

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


def majVariablesGestion():
    """
    Lit les valeurs du fichier gestion.txt et les retourne
    """

    fichier_gestion = open(chemin_gestion, "r")
    contenu_fichier = fichier_gestion.read()
    destinataire = contenu_fichier.split(";")[0]
    telephone = contenu_fichier.split(";")[1]
    etat_appli = contenu_fichier.split(";")[2]
    fichier_gestion.close()

    return destinataire, telephone, etat_appli


def purgeAnciennesVideosPhotos():
    """
    Purge les vidéos et les photos anciennes de plus de 31 jours
    Le traitement s'effectue au lancement de la caméra, puis une fois par jour si la caméra est active
    """

    global regex_jour
    global date_courante

    date_courante = time.strftime("%Y_%m_%d")

    for root, dirs, files in os.walk(chemin_enregistrements):
        if len(dirs):
            for dir in dirs:
                if regex_date.match(dir):
                    date_dir = datetime.strptime(dir, "%Y_%m_%d")
                    date_limite = datetime.strptime(date_courante, "%Y_%m_%d") - timedelta(days=31)

                    if date_dir < date_limite:
                        path = os.path.join(root, dir)
                        shutil.rmtree(path, ignore_errors=True)


# *************************** Partie IA tensorflow *************************************

# Lecture du modèle qui a déjà été entrainé avec le dataset COCO
detection_graph = tf.Graph()
with detection_graph.as_default():
    od_graph_def = tf.GraphDef()
    # Recupère le modèle
    with tf.gfile.GFile(chemin_graphe, 'rb') as fid:
        serialized_graph = fid.read()
        od_graph_def.ParseFromString(serialized_graph)
        # Importe od_graph_def dans le graph courant
        tf.import_graph_def(od_graph_def, name='')

with detection_graph.as_default():
    with tf.Session() as sess:
        # Récupére les images de la source
        cap = cv2.VideoCapture(source_video)
        # Retourne la liste des opérations dans le graphe
        ops = tf.get_default_graph().get_operations()
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

        while etat_appli == "true":

            # Mise à jour des variables de gestion
            destinataire, telephone, etat_appli = majVariablesGestion()

            # Purge des anciennes photos et vieilles vidéos
            if date_courante is None or date_courante != time.strftime("%Y_%m_%d"):
                purgeAnciennesVideosPhotos()

            # Lit les images provenant de la source vidéo
            ret, frame = cap.read()
            hauteur, largeur, nbr_couche = frame.shape
            output_dict = sess.run(tensor_dict, feed_dict={
                # Donne notre image au réseau de neurones
                image_tensor: np.expand_dims(frame, 0)})

            # On lance la mise à jour de la hashmap des objets
            majClassesHashmap(output_dict)

            # On parcourt les objets de la hashmap objets
            for objets_classe in classes_hashmap:
                for id, objet in classes_hashmap[objets_classe].items():

                    id_objet = id
                    coord = objet.get_coord()
                    cpt_fin_mouvement = objet.get_cpt_fin_mouvement()
                    cpt_confirmation_detection = objet.get_cpt_confirm_detection()

                    height, width = frame.shape[:2]
                    xmin = int(coord[0] * width)
                    xmax = int(coord[1] * width)
                    ymin = int(coord[2] * height)
                    ymax = int(coord[3] * height)

                    # Traitement des personnes
                    if objets_classe == 1:

                        # Si l'objet est confirmé
                        if cpt_confirmation_detection == 0:

                            # Détection des visages
                            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                            face = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=4,
                                                                 minSize=(min_size, min_size))

                            if objet.get_num_premiere_photo() is None:
                                objet.set_num_premiere_photo(cpt_photos_temp)

                            for x, y, w, h in face:
                                # Si le visage est compris dans la zone de détection de la personne
                                if x >= xmin and x + w <= xmax and y >= ymin and y + h <= ymax:
                                    roi_gray = cv2.resize(gray[y:y + h, x:x + w], (var_algo.min_size, var_algo.min_size))
                                    id_, conf = recognizer.predict(roi_gray)

                                    # Si on reconnait le visage
                                    if conf <= 95:
                                        # TODO: mettre en place un compteur pour confirmer la détection sur plusieurs frames ?
                                        objet.set_reconnu(True)
                                        cpt_personnes_inconnues -= 1

                            # Calcule le nombre d'images que l'objet est présent sur l'écran
                            if objet.get_num_premiere_photo() <= cpt_photos_temp:
                                nb_frame = cpt_photos_temp - objet.get_num_premiere_photo()
                            else:
                                nb_frame = longueur_video - objet.get_num_premiere_photo() + cpt_photos_temp

                            # Si l'objet est disparu depuis fin_mouvement ou qu'on a atteint la taille max de la vidéo
                            if objet.get_cpt_fin_mouvement() == 0 or nb_frame == longueur_video - 1:

                                # Si la personne n'a pas été reconnue et qu'il n'y a pas déjà eu notification
                                # On crée un fichier vidéo
                                if not(objet.get_reconnu()) and not(objet.get_alerte_envoyee()):

                                    # Récupére le répertoire concernant la personne détectée
                                    dir_videos = chemin_humains

                                    temps = time
                                    jour = temps.strftime("%Y_%m_%d")
                                    # Crée le repertoire du jour courant s'il n'existe pas
                                    if not os.path.isdir(dir_videos + jour):
                                        os.mkdir(dir_videos + jour)

                                    # Met à jour le répertoire ou il faut enregistrer l'image de l'animal
                                    dir_videos = dir_videos + jour + "/"

                                    objet.set_chemin_fichier(
                                        dir_videos + temps.strftime("%Y_%m_%d_%H_%M_%S") + ".avi")
                                    video = cv2.VideoWriter(objet.get_chemin_fichier(),
                                                            cv2.VideoWriter_fourcc(*'DIVX'), video_fps, (largeur, hauteur))
                                    liste_images = []
                                    compteur_photo_personne = objet.get_num_premiere_photo()

                                    # On parcourt et on stocke chaque image ou la personne était présente sur l'écran
                                    while compteur_photo_personne != cpt_photos_temp:

                                        liste_images.append(chemin_photos_temp + str(compteur_photo_personne) + ".png")
                                        if compteur_photo_personne == longueur_video:
                                            compteur_photo_personne = 0
                                        compteur_photo_personne += 1

                                    # On écrit chaque image dans la vidéo
                                    for img in liste_images:
                                        my_image = cv2.imread(img)
                                        video.write(my_image)

                                    video.release()

                                    # On envoie la notif
                                    nom_video = objet.get_chemin_fichier().split("/")[-1]
                                    dir_videos = objet.get_chemin_fichier().replace(nom_video, "")
                                    envoi_mail.envoyerMail(destinataire, "Alerte",
                                                           "Une personne inconnue a été détectée",
                                                           dir_videos, nom_video)
                                    envoi_sms.envoyerSms(telephone, "Une personne inconnue a été détectée.")

                                    # Récupération du fichier json des notifications
                                    notifications_json = open(chemin_notifications_json, "wt")
                                    myjson = json.loads(notifications_json.read())

                                    # Récupération du tableau des notifications
                                    tableau_notifications = notifications.get("notifications")

                                    # Nouvelle notification
                                    notif = {
                                        "status": 0,
                                        "date": temps.strftime("%Y/%m/%d %H:%M:%S"),
                                        "path": dir_videos + nom_video,
                                        "type": "humain"
                                    }

                                    # Ajout de la notification dans le json
                                    tableau_notifications.append(notif)
                                    notifications = json.dumps(myjson)
                                    notifications_json.write(notifications)
                                    notifications_json.close()

                                    objet.set_alerte_envoyee(True)
                                    cpt_personnes_inconnues -= 1

                            objet.set_cpt_fin_mouvement(objet.get_cpt_fin_mouvement() - 1)

                        # Traitement des animaux
                        if objets_classe in {16, 17, 18, 19, 20, 21, 22, 23, 24, 25}:

                            fichier_photo = objet.get_chemin_fichier()

                            # Si l'objet est confirmé
                            if cpt_confirmation_detection == 0:

                                # Récupére le répertoire concernant l'animal détecté
                                dir_photos = chemin_animaux

                                temps = time
                                # Crée le repertoire du jour courant s'il n'existe pas
                                if not os.path.isdir(dir_photos + temps.strftime("%Y_%m_%d")):
                                    os.mkdir(dir_photos + temps.strftime("%Y_%m_%d"))

                                # Met à jour le répertoire ou il faut enregistrer l'image de l'animal
                                dir_photos = dir_photos + temps.strftime("%Y_%m_%d") + "/"

                                # On crée un fichier photo
                                if fichier_photo is None:
                                    nom_photo = temps.strftime("%Y_%m_%d_%H_%M_%S") + ".png"
                                    fichier_photo = dir_photos + nom_photo
                                    objet.set_chemin_fichier(fichier_photo)
                                    cv2.imwrite(fichier_photo, frame)

                            if objet.get_cpt_fin_mouvement() == 0:
                                nom_photo = objet.get_chemin_fichier().split("/")[-1]
                                dir_photos = objet.get_chemin_fichier().replace(nom_photo, "")
                                envoi_mail.envoyerMail(destinataire, "Détection animal", "Un animal sauvage a été détecté",
                                                       dir_photos, nom_photo)
                                envoi_sms.envoyerSms(telephone, "Un animal sauvage a été détecté.")
                                objet.set_chemin_fichier(None)

                                # Récupération du fichier json des notifications
                                notifications_json = open(chemin_notifications_json, "wt")
                                myjson = json.loads(notifications_json.read())

                                # Récupération du tableau des notifications
                                tableau_notifications = notifications.get("notifications")

                                # Nouvelle notification
                                notif = {
                                    "status": 0,
                                    "date": temps.strftime("%Y/%m/%d %H:%M:%S"),
                                    "path": dir_photos + nom_photo,
                                    "type": "animal"
                                }

                                # Ajout de la notification dans le json
                                tableau_notifications.append(notif)
                                notifications = json.dumps(myjson)
                                notifications_json.write(notifications)
                                notifications_json.close()

                            objet.set_cpt_fin_mouvement(objet.get_cpt_fin_mouvement() - 1)

            # Enregistrement des images tmp
            if cpt_personnes_inconnues != 0:
                nom_photo = str(cpt_photos_temp) + ".png"
                fichier_photo = chemin_photos_temp + nom_photo

                if cpt_photos_temp == longueur_video:
                    if os.path.exists("0.png"):
                        os.remove("0.png")
                else:
                    cv2.imwrite(fichier_photo, frame)
            else:
                for root, dirs, files in os.walk(chemin_photos_temp):
                    for file in files:
                        if os.path.exists(os.path.join(root, file)):
                            os.remove(os.path.join(root, file))

            if cpt_photos_temp == longueur_video:
                cpt_photos_temp = 0

            cpt_photos_temp += 1

        cap.release()
