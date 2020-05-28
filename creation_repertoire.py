import os

tableau_chemins = [
    "media",
    "media/photos_temp",
    "media/personnes_connues",
    "media/enregistrement_journalier",
    "media/enregistrement_journalier/humains",
    "media/enregistrement_journalier/animaux",
]

for chemin in tableau_chemins:
    if not os.path.isdir(chemin):
        os.mkdir(chemin)
