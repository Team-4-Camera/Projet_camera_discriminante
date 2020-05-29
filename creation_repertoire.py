import os
import variables_algo as var_algo

repertoire_courant = var_algo.repertoire_courant

tableau_chemins = [
    "..\\media",
    "..\\media\\photos_temp",
    "..\\media\\personnes_connues",
    "..\\media\\enregistrement_journalier",
    "..\\media\\enregistrement_journalier\\humains",
    "..\\media\\enregistrement_journalier\\animaux",
]

for chemin in tableau_chemins:
    if not os.path.isdir(repertoire_courant+chemin):
        os.mkdir(repertoire_courant+chemin)
