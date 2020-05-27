import pickle

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
    90: "toothbrush",
    91: "animal"
}

# le répertoire dans lequel sont enregistrés les photos des animaux
chemin_animaux = "media/enregistrement_journalier/animaux/"
# le répertoire dans lequel sont enregistrés les vidéos des humains
chemin_humains = "media/enregistrement_journalier/humains/"
# le répertoire dans lequel sont enregistrées les photos de création de vidéo
chemin_photos_temp = "media/photos_temp/"
# le modèle COCO utilisé pour la détection des personnes et des animaux
modele_detection = 'ssd_mobilenet_v2_coco_2018_03_29'
# son graphe associé
chemin_graphe = modele_detection + '/frozen_inference_graph.pb'
# Chemin pour accéder au gestion.txt
chemin_gestion = "C:/wamp64/www/projet_camera/Application_web_camera_discriminante/gestion_site/gestion.txt"

# un compteur d'images avant de confirmer la détection des objets sur l'image
confirmation_detection = 5
# l'indice de confiance minimum pour détecter un objet
precision_retenue = 0.50
# le nombre d'images sans détection avant de couper la vidéo
fin_mouvement = 16
# le nombre d'images que comportera la vidéo
longueur_video = 160
# Le pourcentage d'écart permis entre deux coordonnées pour être détecté comme un seul objet
coord_pourcentage = 20
# Les fps de la vidéo à enregistrer
video_fps = 8

# taille minimum de l'image
min_size = 70
