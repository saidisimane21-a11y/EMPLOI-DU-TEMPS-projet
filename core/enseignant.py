from core.creneau import Creneau


class Enseignant:
    """
    Représente un enseignant avec ses matières et ses disponibilités.
    """

    def __init__(self, identifiant: int, nom: str, matieres=None, disponibilites=None):
        self._valider_identifiant(identifiant)
        self._valider_nom(nom)

        self._id = identifiant
        self._nom = nom
        self._matieres = list(matieres) if matieres else []
        self._disponibilites = list(disponibilites) if disponibilites else []

    # Propriétés (lecture seule)

    @property
    def id(self):
        return self._id

    @property
    def nom(self):
        return self._nom

    @property
    def matieres(self):
        return list(self._matieres)

    @property
    def disponibilites(self):
        return list(self._disponibilites)

    # Logique métier

    def est_disponible(self, creneau: Creneau) -> bool:
        """
        Vérifie si le créneau demandé est inclus
        dans au moins une disponibilité de l'enseignant.
        """
        if not isinstance(creneau, Creneau):
            raise TypeError("creneau doit être une instance de Creneau")

        return any(
            dispo.contient(creneau) for dispo in self._disponibilites
        )
    def ajouter_disponibilite(self, creneau):
      self._disponibilites.append(creneau)

    # Validation interne

    def _valider_identifiant(self, identifiant):
        if not isinstance(identifiant, int) or identifiant <= 0:
            raise ValueError(
                "L'identifiant de l'enseignant doit être un entier positif.")

    def _valider_nom(self, nom):
        if not isinstance(nom, str) or not nom.strip():
            raise ValueError(
                "Le nom de l'enseignant doit être une chaîne non vide.")

    # Représentation

    def __str__(self):
        return f"Enseignant {self.nom}"

    def __eq__(self, autre):
        if not isinstance(autre, Enseignant):
            return False
        return self.id == autre.id

    def __hash__(self):
        return hash(self.id)
