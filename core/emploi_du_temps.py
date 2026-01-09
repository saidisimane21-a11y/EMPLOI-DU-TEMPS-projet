from core.seance import Seance


class EmploiDuTemps:
    """
    Contient la liste des séances et gère l'ajout avec vérification des conflits.
    """

    def __init__(self):
        self._seances = []

    # --------------------
    # Propriétés
    # --------------------
    @property
    def seances(self):
        return list(self._seances)

    # --------------------
    # Gestion des séances
    # --------------------
    def ajouter_seance(self, nouvelle_seance: Seance):
        """
        Ajoute une séance si aucun conflit n'est détecté.
        """
        if self.verifier_conflit(nouvelle_seance):
            raise ValueError("Conflit détecté : la séance ne peut pas être ajoutée.")
        self._seances.append(nouvelle_seance)

    def verifier_conflit(self, s: Seance) -> bool:
        """
        Vérifie si une séance entre en conflit avec les séances existantes.
        Conflits possibles :
        - Même créneau pour la même salle
        - Même créneau pour le même enseignant
        - Même créneau pour le même groupe
        """
        for existante in self._seances:
            if existante.creneau == s.creneau:
                if (
                    existante.salle == s.salle
                    or existante.enseignant == s.enseignant
                    or existante.groupe == s.groupe
                ):
                    return True
        return False

    # --------------------
    # Recherche / Consultation
    # --------------------
    def seances_par_groupe(self, groupe_nom: str):
        return [s for s in self._seances if s.groupe.nom == groupe_nom]

    def seances_par_enseignant(self, enseignant_nom: str):
        return [s for s in self._seances if s.enseignant.nom == enseignant_nom]

    def seances_par_salle(self, salle_nom: str):
        return [s for s in self._seances if s.salle.nom == salle_nom]

    # --------------------
    # Représentation
    # --------------------
    def __str__(self):
        return "\n".join(str(s) for s in self._seances)
