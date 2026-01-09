from users.utilisateur import Utilisateur

class Etudiant(Utilisateur):
    """
    Profil étudiant : peut consulter l'emploi du temps de son groupe.
    """

    def __init__(self, username, password, groupe):
        super().__init__(username, password)
        self.groupe = groupe  # instance de core.groupe.GroupeEtudiant

    def consulter_emploi_du_temps(self, emploi_du_temps):
        return emploi_du_temps.seances_par_groupe(self.groupe.nom)
