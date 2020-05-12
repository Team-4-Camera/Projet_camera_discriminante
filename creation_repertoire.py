import os

tableau_chemins = {
    "photos",
    "photos/personnes_connues",
    "photos/enregistrement_journalier",
    "photos/enregistrement_journalier/humains",
    "photos/enregistrement_journalier/animaux",
    "photos/enregistrement_journalier/animaux/oiseaux",
    "photos/enregistrement_journalier/animaux/chats",
    "photos/enregistrement_journalier/animaux/chiens",
    "photos/enregistrement_journalier/animaux/chevaux",
    "photos/enregistrement_journalier/animaux/moutons",
    "photos/enregistrement_journalier/animaux/vaches",
    "photos/enregistrement_journalier/animaux/elephants",
    "photos/enregistrement_journalier/animaux/ours",
    "photos/enregistrement_journalier/animaux/zebres",
    "photos/enregistrement_journalier/animaux/girafes"
}

for chemin in tableau_chemins:
    if not os.path.isdir(chemin):
        os.mkdir(chemin)
