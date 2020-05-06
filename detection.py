import numpy as np
import tensorflow.compat.v1 as tf
import cv2
import time

tf.disable_v2_behavior()

labels = {
    1: "person",
    2: "bicycle",
    3: "car",
    4: "motorcycle",
    5: "airplane",
    6: "bus",
    7: "train",
    8: "truck",
    9: "boat",
    10: "traffic light",
    11: "fire hydrant",
    13: "stop sign",
    14: "parking meter",
    15: "bench",
    16: "bird",
    17: "cat",
    18: "dog",
    19: "horse",
    20: "sheep",
    21: "cow",
    22: "elephant",
    23: "bear",
    24: "zebra",
    25: "giraffe",
    27: "backpack",
    28: "umbrella",
    31: "handbag",
    32: "tie",
    33: "suitcase",
    34: "frisbee",
    35: "skis",
    36: "snowboard",
    37: "sports ball",
    38: "kite",
    39: "baseball bat",
    40: "baseball glove",
    41: "skateboard",
    42: "surfboard",
    43: "tennis racket",
    44: "bottle",
    46: "wine glass",
    47: "cup",
    48: "fork",
    49: "knife",
    50: "spoon",
    51: "bowl",
    52: "banana",
    53: "apple",
    54: "sandwich",
    55: "orange",
    56: "broccoli",
    57: "carrot",
    58: "hot dog",
    59: "pizza",
    60: "donut",
    61: "cake",
    62: "chair",
    63: "couch",
    64: "potted plant",
    65: "bed",
    67: "dining table",
    70: "toilet",
    72: "tv",
    73: "laptop",
    74: "mouse",
    75: "remote",
    76: "keyboard",
    77: "cell phone",
    78: "microwave",
    79: "oven",
    80: "toaster",
    81: "sink",
    82: "refrigerator",
    84: "book",
    85: "clock",
    86: "vase",
    87: "scissors",
    88: "teddy bear",
    89: "hair drier",
    90: "toothbrush"
}

MODEL_NAME = 'ssd_mobilenet_v2_coco_2018_03_29'
PATH_TO_FROZEN_GRAPH = MODEL_NAME + '/frozen_inference_graph.pb'
color_infos = (255, 255, 0)
fichier_video = None
cpt_fin_mouvement = -1

# variables parametrables
dir_videos = "c:\\enregistrements\\"
precision_retenue = 0.50
fin_mouvement = 40


# *************************** Partie IA tensorflow *************************************

# Lecture du modèle qui a déjà été entrainée avec le dataset COCO
detection_graph = tf.Graph()
with detection_graph.as_default():
    od_graph_def = tf.GraphDef()
    # Recupère le modèle
    with tf.gfile.GFile(PATH_TO_FROZEN_GRAPH, 'rb') as fid:
        serialized_graph = fid.read()
        od_graph_def.ParseFromString(serialized_graph)
        # importer od_graph_def dans le graph courant
        tf.import_graph_def(od_graph_def, name='')

with detection_graph.as_default():
    with tf.Session() as sess:
        # cap=cv2.VideoCapture('video1.mp4')
        cap = cv2.VideoCapture(0)  # récupére les images de la webcam intégré
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
            nbr_object = int(output_dict['num_detections'])  # nombre d'objets présents
            classes = output_dict['detection_classes'][0].astype(np.uint8)  # le tableau avec les identifiants
            boxes = output_dict['detection_boxes'][0]  # les coordonnées localisant les objets
            scores = output_dict['detection_scores'][0]  # indice de confiance renvoyé pour chaque objet

            for objet in range(nbr_object):  # on parcourt tous les objets détectés sur l'image
                ymin, xmin, ymax, xmax = boxes[objet]

                if scores[objet] > precision_retenue:  # si le score est supérieur au paramétrage
                    if classes[objet] in {1, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25}:
                        height, width = frame.shape[:2]
                        xmin = int(xmin * width)
                        xmax = int(xmax * width)
                        ymin = int(ymin * height)
                        ymax = int(ymax * height)
                        cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), color_infos, 1)
                        txt = "{:s}:{:3.0%}".format(labels[classes[objet]], scores[objet])
                        cv2.putText(frame, txt, (xmin, ymin - 5), cv2.FONT_HERSHEY_PLAIN, 1, color_infos, 2)

                    if classes[objet] in {16, 17, 18, 19, 20, 21, 22, 23, 24, 25}:  # si un animal est détecté
                        # on crée un fichier video s'il s'agit de la premiere image enregistrée
                        if fichier_video is None:
                            fichier_video = dir_videos + time.strftime("%Y_%m_%d_%H_%M_%S") + ".avi"
                            video = cv2.VideoWriter(fichier_video, cv2.VideoWriter_fourcc(*'DIVX'), 15,
                                                    (largeur, hauteur))

                        cpt_fin_mouvement = fin_mouvement  # on initialise ou réinitialise le compteur

            if cpt_fin_mouvement > 0:
                video.write(frame)  # on écrit dans la video tant que le compteur n'atteint pas 0

            if cpt_fin_mouvement == 0:
                video.release()  # on cloture la video si aucun animal n'a été détecté depuis cpt_fin_mouvement images
                fichier_video = None

            cpt_fin_mouvement = cpt_fin_mouvement - 1

            cv2.imshow('image', frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('a'):
                for objet in range(500):
                    ret, frame = cap.read()
            if key == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
