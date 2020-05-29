import json
import os
import variables_algo as algo

chemin_notifications_json = algo.chemin_notifications_json
if not os.path.isfile(chemin_notifications_json):
    notifications = json.dumps({
        "notifications": []
    })
    fichier = open(chemin_notifications_json, "wt")
    fichier.write(notifications)
    fichier.close()
