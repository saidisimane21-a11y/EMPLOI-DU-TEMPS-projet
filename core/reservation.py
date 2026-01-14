class Reservation:
    """
    Représente une demande de réservation d'une salle par un enseignant.
    """

    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"

    def __init__(self, enseignant, salle, creneau):
        self._enseignant = enseignant
        self._salle = salle
        self._creneau = creneau
        self._statut = Reservation.PENDING

    # --------------------
    # Propriétés (lecture seule)
    # --------------------
    @property
    def enseignant(self):
        return self._enseignant

    @property
    def salle(self):
        return self._salle

    @property
    def creneau(self):
        return self._creneau

    @property
    def statut(self):
        return self._statut

    # --------------------
    # Gestion du statut
    # --------------------
    def accepter(self):
        self._statut = Reservation.ACCEPTED

    def rejeter(self):
        self._statut = Reservation.REJECTED

    # --------------------
    # Représentation
    # --------------------
    def __str__(self):
        return (
            f"Réservation({self.salle.nom}, "
            f"{self.creneau}, "
            f"{self.enseignant.nom}, "
            f"statut={self.statut})"
        )
