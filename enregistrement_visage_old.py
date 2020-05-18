import cv2
import operator

face_cascade=cv2.CascadeClassifier("./haarcascade_frontalface_alt2.xml")
# Create a VideoCapture object and read from input file 

# 0 pour utiliser la caméra
cap=cv2.VideoCapture(0)


id=0
while True:
    # lire la vidéo image par image
    ret, frame=cap.read()
    gray=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    face=face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=4, minSize=(algo.min_size, algo.min_size))
    # récupérer le visage via un quadruplet
    for x, y, w, h in face:
        cv2.imwrite("non-classees/p-{:d}.png".format(id), frame[y:y+h, x:x+w])
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
        id+=1
    key=cv2.waitKey(5)
    # quitter
    if key==ord('q'):
        break
    # lire sans image (avance rapide)
    if key==ord('a'):
        for cpt in range(100):
            ret, frame=cap.read()
    cv2.imshow('video', frame)
    for cpt in range(4):
        ret, frame=cap.read()
cap.release()
cv2.destroyAllWindows()
