import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


def envoyerMail(toadd, subject, msg, chemin_fichiers, nom_fichier):
    """
    Envoie un mail à un destinataire avec un message, un sujet
    Peut contenir une pièce jointe
    Param : toadd : l'adresse mail du destinataire
            subject : le sujet du mail
            msg : le message contenu dans le mail
            chemin_fichier : le chemin vers la pièce jointe à ajouter
            nom_fichier : le nom de la pièce jointe à ajouter
    """

    fromadd = "cameradiscriminante@gmail.com"
    # Création de l'objet "message"
    message = MIMEMultipart()
    # Spécification de l'expéditeur
    message['From'] = fromadd
    # Attache du destinataire à l'objet "message"
    message['To'] = toadd
    # Spécification de l'objet de votre mail
    message['Subject'] = subject
    # Attache du message à l'objet "message", et encodage en UTF-8
    message.attach(MIMEText(msg.encode('utf-8'), 'plain', 'utf-8'))

    # Ouverture du fichier
    piece = open(chemin_fichiers + nom_fichier, "rb")
    # Encodage de la pièce jointe en Base64
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(piece.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "piece; filename= %s" % nom_fichier)
    # Attache de la pièce jointe à l'objet "message"
    message.attach(part)

    # Connexion au serveur sortant
    serveur = smtplib.SMTP('smtp.gmail.com', 587)
    # Spécification de la sécurisation
    serveur.starttls()
    # Authentification
    serveur.login(fromadd, "superprojet")
    # Conversion de l'objet "message" en chaine de caractère et encodage en UTF-8
    texte = message.as_string().encode('utf-8')

    # Envoi du mail
    serveur.sendmail(fromadd, toadd, texte)
    # Déconnexion du serveur
    serveur.quit()
