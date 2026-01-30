from users.utilisateur import Utilisateur
from core.reservation import Reservation


class Administrateur(Utilisateur):
    """
    Administrateur : gère manuellement l'emploi du temps et les réservations.
    """

    def __init__(self, username: str, password: str, emploi_du_temps):
        super().__init__(username, password)
        self._emploi_du_temps = emploi_du_temps

    # --------------------
    # Propriétés
    # --------------------
    @property
    def nom(self):
        """Retourne le nom d'utilisateur pour compatibilité avec l'interface."""
        return self.username

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

