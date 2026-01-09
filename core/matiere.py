class Matiere:
    """
    Représente une matière enseignée dans l'établissement.
    """

    TYPES_SEANCE_VALIDES = {"cours", "td", "tp"}

    def __init__(
        self,
        code: str,
        nom: str,
        type_seance: str,
        volume_horaire: int,
        equipements_requis=None
    ):
        self._valider_code(code)
        self._valider_nom(nom)
        self._valider_type_seance(type_seance)
        self._valider_volume(volume_horaire)

        self._code = code.upper()
        self._nom = nom
        self._type_seance = type_seance.lower()
        self._volume_horaire = volume_horaire
        self._equipements_requis = set(equipements_requis) if equipements_requis else set()

    # --------------------
    # Propriétés (lecture seule)
    # --------------------
    @property
    def code(self):
        return self._code

    @property
    def nom(self):
        return self._nom

    @property
    def type_seance(self):
        return self._type_seance

    @property
    def volume_horaire(self):
        return self._volume_horaire

    @property
    def equipements_requis(self):
        return set(self._equipements_requis)

    # --------------------
    # Validation interne
    # --------------------
    def _valider_code(self, code):
        if not isinstance(code, str) or not code.strip():
            raise ValueError("Le code de la matière doit être une chaîne non vide.")

    def _valider_nom(self, nom):
        if not isinstance(nom, str) or not nom.strip():
            raise ValueError("Le nom de la matière doit être une chaîne non vide.")

    def _valider_type_seance(self, type_seance):
        if type_seance.lower() not in self.TYPES_SEANCE_VALIDES:
            raise ValueError(
                f"Type de séance invalide : {type_seance}. "
                f"Types autorisés : {self.TYPES_SEANCE_VALIDES}"
            )

    def _valider_volume(self, volume):
        if not isinstance(volume, int) or volume <= 0:
            raise ValueError("Le volume horaire doit être un entier strictement positif.")


    # Représentation
  
    def __str__(self):
        return f"{self.code} - {self.nom} ({self.type_seance})"

    def __eq__(self, autre):
        if not isinstance(autre, Matiere):
            return False
        return self.code == autre.code

    def __hash__(self):
        return hash(self.code)
