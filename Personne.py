import EtreVivant


class Personne(EtreVivant):

    def __init__(self, coord, cpt_fin_mouvement, chemin_fichier, cpt_confirm_detection, reconnu, cpt_frame_video):
        self.__coord = coord
        self.__cpt_fin_mouvement = cpt_fin_mouvement
        self.__chemin_fichier = chemin_fichier
        self.__cpt_confirm_detection = cpt_confirm_detection
        self.__reconnu = reconnu
        self.__cpt_frame_video = cpt_frame_video

    def get_reconnu(self):
        return self.__reconnu

    def get_cpt_frame_video(self):
        return self.__cpt_frame_video

    def set_reconnu(self, reconnu):
        self.__reconnu = reconnu

    def set_cpt_frame_video(self, cpt_frame_video):
        self.__cpt_frame_video = cpt_frame_video
