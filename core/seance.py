from core.creneau import Creneau
from core.salle import Salle
from core.matiere import Matiere
from core.groupe import GroupeEtudiant
from core.enseignant import Enseignant


class Seance:
    """
    Représente une séance dans l'emploi du temps.
    Lie : matière, enseignant, groupe, salle et créneau.
    """

    def __init__(
        self,
        matiere: Matiere,
        enseignant: Enseignant,
        groupe: GroupeEtudiant,
        salle: Salle,
        creneau: Creneau
    ):
        self._matiere = matiere
        self._enseignant = enseignant
        self._groupe = groupe
        self._salle = salle
        self._creneau = creneau

        self._valider_compatibilite()

    # --------------------
    # Propriétés (lecture seule)
    # --------------------
    @property
    def matiere(self):
        return self._matiere

    @property
    def enseignant(self):
        return self._enseignant

    @property
    def groupe(self):
        return self._groupe

    @property
    def salle(self):
        return self._salle

    @property
    def creneau(self):
        return self._creneau

    # --------------------
    # Validation interne
    # --------------------
    def _valider_compatibilite(self):
        """
        Vérifie que la séance est possible selon l'effectif et les équipements.
        """
        if not self.salle.est_compatible(self.groupe.effectif, self.matiere.equipements_requis):
            raise ValueError(
                f"La salle {self.salle.nom} n'est pas compatible avec le groupe "
                f"{self.groupe.nom} ou la matière {self.matiere.nom}."
            )

    # --------------------
    # Représentation
    # --------------------
    def __str__(self):
        return (
            f"{self.matiere.nom} avec {self.enseignant.nom} "
            f"pour {self.groupe.nom} en {self.salle.nom} ({self.creneau})"
        )

    def __eq__(self, autre):
        if not isinstance(autre, Seance):
            return False
        return (
            self.matiere == autre.matiere
            and self.enseignant == autre.enseignant
            and self.groupe == autre.groupe
            and self.salle == autre.salle
            and self.creneau == autre.creneau
        )

    def __hash__(self):
        return hash((self.matiere, self.enseignant, self.groupe, self.salle, self.creneau))
