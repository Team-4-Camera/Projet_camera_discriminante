# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client

import sys

telephone = ( sys.argv[1] )
code      = ( sys.argv[2] )

# Your Account Sid and Auth Token from twilio.com/console
# DANGER! This is insecure. See http://twil.io/secure
account_sid = 'ACe452c77962317112730133dfaea130fd'
auth_token  = '3af09c56a1967df682d6079b4cc12e03'
client      = Client(account_sid, auth_token)

message     = client.messages \
                .create(
                     body=code+" est le code pour rénitialisation de votre mot de passe.",
                     from_='+12025190312',
                     to=telephone
                 )

print(message.sid)