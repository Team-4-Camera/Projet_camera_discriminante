# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client

# Your Account Sid and Auth Token from twilio.com/console
# DANGER! This is insecure. See http://twil.io/secure
account_sid = 'ACe452c77962317112730133dfaea130fd'
auth_token = '3af09c56a1967df682d6079b4cc12e03'
client = Client(account_sid, auth_token)


def envoyerSms(toadd, msg):
    """
    Envoie un SMS à un destinataire avec un message
    Param : toadd : le numéro du destinataire, commençant par +33
            msg : le message du sms
    """

    message = client.messages.create(body=msg, from_='+12025190312', to=toadd)

    print(message.sid)
