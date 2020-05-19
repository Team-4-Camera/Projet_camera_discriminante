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
#cap = cv2.VideoCapture(sys.argv[1])
cap = cv2.VideoCapture(0)
#chemin_enregistrement = 'photos/personnes_connues/' + sys.argv[2]
chemin_enregistrement = 'photos/personnes_connues/robin/'

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
        # TODO: supprimer la création des rectangles qui ne sert que pour nos tests
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
        id += 1
    # TODO: supprimer la gestion des keys qui ne sert que pour nos tests
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    if key == ord('a'):
        for cpt in range(100):
            ret, frame = cap.read()
    # TODO: supprimer l'affichage de la fenetre de la vidéo qui ne sert que pour nos tests
    cv2.imshow('video', frame)
    for cpt in range(entre_deux_images):
        ret, frame = cap.read()

cap.release()
# TODO: supprimer la destruction de la fenetre qui ne sert que pour nos tests
cv2.destroyAllWindows()
# TODO: supprimer la vidéo après le traitement