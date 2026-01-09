class Salle:
    """
    Représente une salle physique (TD, TP ou Amphithéâtre).
    """

    TYPES_VALIDES = {"amphi", "td", "tp"}

    def __init__(self, identifiant: int, nom: str, capacite: int,
                 type_salle: str, equipements=None):

        self._valider_identifiant(identifiant)
        self._valider_nom(nom)
        self._valider_capacite(capacite)
        self._valider_type(type_salle)

        self._id = identifiant
        self._nom = nom
        self._capacite = capacite
        self._type = type_salle.lower()
        self._equipements = set(equipements) if equipements else set()

  
    # Propriétés (lecture seule)
    
    @property
    def id(self):
        return self._id

    @property
    def nom(self):
        return self._nom

    @property
    def capacite(self):
        return self._capacite

    @property
    def type(self):
        return self._type

    @property
    def equipements(self):
        return set(self._equipements)

  
    # Logique métier
    
    def est_compatible(self, effectif: int, equipements_requis=None) -> bool:
        """
        Vérifie si la salle peut accueillir un groupe et répondre aux besoins matériels.
        """
        if effectif > self.capacite:
            return False

        if equipements_requis:
            return set(equipements_requis).issubset(self._equipements)

        return True

    
    # Validation interne
  
    def _valider_identifiant(self, identifiant):
        if not isinstance(identifiant, int) or identifiant <= 0:
            raise ValueError("L'identifiant de la salle doit être un entier positif.")

    def _valider_nom(self, nom):
        if not isinstance(nom, str) or not nom.strip():
            raise ValueError("Le nom de la salle doit être une chaîne non vide.")

    def _valider_capacite(self, capacite):
        if not isinstance(capacite, int) or capacite <= 0:
            raise ValueError("La capacité doit être un entier strictement positif.")

    def _valider_type(self, type_salle):
        if type_salle.lower() not in self.TYPES_VALIDES:
            raise ValueError(
                f"Type de salle invalide : {type_salle}. "
                f"Types autorisés : {self.TYPES_VALIDES}"
            )

    
    # Représentation
    
    def __str__(self):
        return f"{self.nom} ({self.type}, capacité {self.capacite})"

    def __eq__(self, autre):
        if not isinstance(autre, Salle):
            return False
        return self.id == autre.id

    def __hash__(self):
        return hash(self.id)
