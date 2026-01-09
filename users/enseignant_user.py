from users.utilisateur import Utilisateur

class EnseignantUser(Utilisateur):
    """
    Profil enseignant pour interagir avec l'application.
    Contient une référence vers l'entité métier Enseignant.
    """

    def __init__(self, username, password, enseignant):
        super().__init__(username, password)
        self.enseignant = enseignant  # instance de core.enseignant.Enseignant

    def consulter_emploi_du_temps(self, emploi_du_temps):
        return emploi_du_temps.seances_par_enseignant(self.enseignant.nom)

    def demander_reservation(self, salle, creneau):
        """
        Crée une demande de réservation ponctuelle.
        Ici on peut juste retourner un dictionnaire simplifié.
        """
        return {
            "enseignant": self.enseignant.nom,
            "salle": salle.nom,
            "creneau": str(creneau),
            "validee": False
        }

    def signaler_indisponibilite(self, creneau):
        """
        Ajoute un créneau d'indisponibilité pour l'enseignant.
        """
        self.enseignant.disponibilites.append(creneau)
