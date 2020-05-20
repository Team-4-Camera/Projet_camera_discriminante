class EtreVivant:

    def __init__(self, coord, cpt_fin_mouvement, chemin_fichier, cpt_confirm_detection):
        self.__coord = coord
        self.__cpt_fin_mouvement = cpt_fin_mouvement
        self.__chemin_fichier = chemin_fichier
        self.__cpt_confirm_detection = cpt_confirm_detection

    def get_coord(self):
        return self.__coord

    def get_cpt_fin_mouvement(self):
        return self.__cpt_fin_mouvement

    def get_chemin_fichier(self):
        return self.__chemin_fichier

    def get_cpt_confirm_detection(self):
        return self.__cpt_confirm_detection

    def set_coord(self, coord):
        self.__coord = coord

    def set_cpt_fin_mouvement(self, cpt_fin_mouvement):
        self.__cpt_fin_mouvement = cpt_fin_mouvement

    def set_chemin_fichier(self, chemin_fichier):
        self.__chemin_fichier = chemin_fichier

    def set_cpt_confirm_detection(self, cpt_confirm_detection):
        self.__cpt_confirm_detection = cpt_confirm_detection
