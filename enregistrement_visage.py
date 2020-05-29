import cv2
import sys
import os
import variables_algo

# le fichier doit être appelé comme suit
# python enregistrement_visage.py XXX.mp4 YYY
# XXX étant le nom de la vidéo et YYY le nom du répertoire dans lequel on stocke les photos (robin par exemple)

face_cascade = cv2.CascadeClassifier("./haarcascade_frontalface_alt2.xml")
# cette utilisation par arguments passés ne permet plus l'utilisation avec une cam de l'ordinateur
# il faut donner une vidéo en paramètre
fichier_video = sys.argv[1]
cap = cv2.VideoCapture(fichier_video)
chemin_enregistrement = '../media/personnes_connues/' + sys.argv[2]

# Variable paramétrable
# définit le nombre d'images qu'on laisse passer entre deux enregistrements d'images quand on lit une vidéo
entre_deux_images = 15

if not os.path.isdir(chemin_enregistrement):
    os.mkdir(chemin_enregistrement)

id = 0
while True:
    ret, frame = cap.read()
    if ret is False:
        break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # détecte des objets de différentes tailles dans l'image d'entrée.
    # les objets détectés sont renvoyés sous forme de liste de rectangles.
    face = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=4,
                                         minSize=(variables_algo.min_size, variables_algo.min_size))
    for x, y, w, h in face:
        cv2.imwrite("{}/p-{:d}.png".format(chemin_enregistrement, id), frame[y:y + h, x:x + w])
        id += 1

    for cpt in range(entre_deux_images):
        ret, frame = cap.read()

cap.release()

os.remove(fichier_video)
