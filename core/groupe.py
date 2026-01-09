class GroupeEtudiant:
    """
    Représente un groupe d'étudiants appartenant à une filière donnée.
    """

    def __init__(
        self,
        identifiant: int,
        nom: str,
        filiere: str,
        effectif: int,
        niveau: str = None
    ):
        self._valider_identifiant(identifiant)
        self._valider_nom(nom)
        self._valider_filiere(filiere)
        self._valider_effectif(effectif)

        self._id = identifiant
        self._nom = nom
        self._filiere = filiere
        self._effectif = effectif
        self._niveau = niveau

    # --------------------
    # Propriétés (lecture seule)
    # --------------------
    @property
    def id(self):
        return self._id

    @property
    def nom(self):
        return self._nom

    @property
    def filiere(self):
        return self._filiere

    @property
    def effectif(self):
        return self._effectif

    @property
    def niveau(self):
        return self._niveau

    # --------------------
    # Validation interne
    # --------------------
    def _valider_identifiant(self, identifiant):
        if not isinstance(identifiant, int) or identifiant <= 0:
            raise ValueError("L'identifiant du groupe doit être un entier positif.")

    def _valider_nom(self, nom):
        if not isinstance(nom, str) or not nom.strip():
            raise ValueError("Le nom du groupe doit être une chaîne non vide.")

    def _valider_filiere(self, filiere):
        if not isinstance(filiere, str) or not filiere.strip():
            raise ValueError("La filière doit être une chaîne non vide.")

    def _valider_effectif(self, effectif):
        if not isinstance(effectif, int) or effectif <= 0:
            raise ValueError("L'effectif du groupe doit être un entier strictement positif.")

    # --------------------
    # Représentation
    # --------------------
    def __str__(self):
        base = f"{self.nom} ({self.filiere}) - {self.effectif} étudiants"
        if self.niveau:
            return f"{base}, niveau {self.niveau}"
        return base

    def __eq__(self, autre):
        if not isinstance(autre, GroupeEtudiant):
            return False
        return self.id == autre.id

    def __hash__(self):
        return hash(self.id)
