class Utilisateur:
    """
    Classe de base pour tous les utilisateurs du système.
    Chaque utilisateur peut consulter son emploi du temps.
    """

    def __init__(self, username: str, password: str, id: int = None):
        self._username = username
        self._password = password  # Pour un vrai projet, stocker un hash !
        self._id = id

    # --------------------
    # Propriétés
    # --------------------
    @property
    def username(self):
        return self._username

    @property
    def id(self):
        return self._id

    @property
    def nom(self):
        """Retourne le nom d'affichage de l'utilisateur."""
        return self._username

    # --------------------
    # Méthodes communes
    # --------------------
    def consulter_emploi_du_temps(self, emploi_du_temps):
        """
        Retourne les séances visibles pour cet utilisateur.
        Cette méthode sera spécialisée dans les classes filles.
        """
        raise NotImplementedError(
            "Cette méthode doit être implémentée dans les classes filles."
        )

    # --------------------
    # Authentification basique
    # --------------------
    def verifier_mot_de_passe(self, mot_de_passe: str) -> bool:
        return self._password == mot_de_passe

    def __str__(self):
        return f"Utilisateur: {self.username}"
