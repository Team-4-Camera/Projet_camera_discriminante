import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

chemin_fichiers = "c:\\enregistrements\\"


def envoyermail(toadd, subject, msg, nom_fichier):
    fromadd = "cameradiscriminante@gmail.com"
    message = MIMEMultipart()  ## Création de l'objet "message"
    message['From'] = fromadd  ## Spécification de l'expéditeur
    message['To'] = toadd  ## Attache du destinataire à l'objet "message"
    message['Subject'] = subject  ## Spécification de l'objet de votre mail
    message.attach(
        MIMEText(msg.encode('utf-8'), 'plain',
                 'utf-8'))  ## Attache du message à l'objet "message", et encodage en UTF-8

    piece = open(chemin_fichiers + nom_fichier, "rb")  ## Ouverture du fichier
    part = MIMEBase('application', 'octet-stream')  ## Encodage de la pièce jointe en Base64
    part.set_payload((piece).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "piece; filename= %s" % nom_fichier)
    message.attach(part)  ## Attache de la pièce jointe à l'objet "message"

    serveur = smtplib.SMTP('smtp.gmail.com', 587)  ## Connexion au serveur sortant (en précisant son nom et son port)
    serveur.starttls()  ## Spécification de la sécurisation
    serveur.login(fromadd, "superprojet")  ## Authentification
    texte = message.as_string().encode(
        'utf-8')  ## Conversion de l'objet "message" en chaine de caractère et encodage en UTF-8
    serveur.sendmail(fromadd, toadd, texte)  ## Envoi du mail
    serveur.quit()  ## Déconnexion du serveur
