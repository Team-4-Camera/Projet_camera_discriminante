from EtreVivant import EtreVivant


class Personne(EtreVivant):

    def __init__(self, coord, cpt_fin_mouvement, chemin_fichier, cpt_confirm_detection, reconnu, num_premiere_photo, alerte_envoyee):
        EtreVivant.__init__(self, coord, cpt_fin_mouvement, chemin_fichier, cpt_confirm_detection)
        self.__reconnu = reconnu
        self.__num_premiere_photo = num_premiere_photo
        self.__alerte_envoyee = alerte_envoyee

    def get_reconnu(self):
        return self.__reconnu

    def get_num_premiere_photo(self):
        return self.__num_premiere_photo

    def get_alerte_envoyee(self):
        return self.__alerte_envoyee

    def set_reconnu(self, reconnu):
        self.__reconnu = reconnu

    def set_num_premiere_photo(self, premiere_photo):
        self.__num_premiere_photo = premiere_photo

    def set_alerte_envoyee(self, alerte_envoyee):
        self.__alerte_envoyee = alerte_envoyee
