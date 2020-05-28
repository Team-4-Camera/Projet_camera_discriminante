import envoi_mail
import envoi_sms
import sys

traitement = sys.argv[1]
destinataire = sys.argv[2]
sujet = sys.argv[3]
message = sys.argv[4]

if traitement == "mail":
    envoi_mail.envoyerMail(destinataire, sujet, message, "", "")
elif traitement == "sms":
    envoi_sms.envoyerSms(destinataire, message)
