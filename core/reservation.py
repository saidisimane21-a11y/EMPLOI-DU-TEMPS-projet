class Reservation:
    """
    Représente une demande de réservation d'une salle par un utilisateur (enseignant ou étudiant).
    """

    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"

    def __init__(self, utilisateur, salle, creneau, motif=""):
        self._utilisateur = utilisateur
        self._salle = salle
        self._creneau = creneau
        self._motif = motif
        self._statut = Reservation.PENDING

    # --------------------
    # Propriétés (lecture seule)
    # --------------------
    @property
    def utilisateur(self):
        return self._utilisateur

    @property
    def salle(self):
        return self._salle

    @property
    def creneau(self):
        return self._creneau

    @property
    def motif(self):
        return self._motif

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
        role = getattr(self.utilisateur, 'role', 'Utilisateur')
        nom = getattr(self.utilisateur, 'username', 'Inconnu')
        return (
            f"Réservation({self.salle.nom}, "
            f"{self.creneau}, "
            f"{role}: {nom}, "
            f"statut={self.statut})"
        )
