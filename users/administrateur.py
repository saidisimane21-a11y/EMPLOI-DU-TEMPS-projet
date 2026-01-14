from users.utilisateur import Utilisateur
from core.reservation import Reservation


class Administrateur(Utilisateur):
    """
    Administrateur : gère manuellement l'emploi du temps et les réservations.
    """

    def __init__(self, identifiant: int, nom: str, emploi_du_temps):
        super().__init__(identifiant, nom)
        self._emploi_du_temps = emploi_du_temps

    # --------------------
    # Gestion des séances
    # --------------------
    def ajouter_seance(self, seance):
        self._emploi_du_temps.ajouter_seance(seance)

    def supprimer_seance(self, seance):
        if seance in self._emploi_du_temps.seances:
            self._emploi_du_temps.seances.remove(seance)

    def consulter_emploi_du_temps(self):
        return self._emploi_du_temps.seances

    # --------------------
    # Gestion des réservations
    # --------------------
    def valider_reservation(self, reservation: Reservation):
        reservation.accepter()

    def rejeter_reservation(self, reservation: Reservation):
        reservation.rejeter()

