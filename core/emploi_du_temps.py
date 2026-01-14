from core.seance import Seance


class EmploiDuTemps:
    """
    Contient la liste des séances et gère l'ajout avec vérification des conflits.
    """

    def __init__(self):
        self._seances = []

    # Propriétés (lecture seule)

    @property
    def seances(self):
        return list(self._seances)

    # Gestion des séances

    def ajouter_seance(self, nouvelle_seance: Seance) -> None:
        """
        Ajoute une séance si aucun conflit n'est détecté.
        """
        if self.verifier_conflit(nouvelle_seance):
            raise ValueError(
                "Conflit détecté : la séance ne peut pas être ajoutée.")
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

  

    # Recherche / Consultation
    def seances_par_groupe(self, groupe_nom: str) -> list:
        return [s for s in self._seances if s.groupe.nom == groupe_nom]

    def seances_par_enseignant(self, enseignant_nom: str) -> list:
        return [s for s in self._seances if s.enseignant.nom == enseignant_nom]

    def seances_par_salle(self, salle_nom: str) -> list:
        return [s for s in self._seances if s.salle.nom == salle_nom]

    # Statistiques
    def calculer_taux_occupation(self, salle) -> float:
        """
        Calcule le taux d'occupation d'une salle en %.
        Taux = (heures occupées / heures totales) * 100
        """
        heures_occupees = sum(
            (s.creneau.heure_fin.hour - s.creneau.heure_debut.hour)
            for s in self._seances if s.salle == salle
        )
        heures_totales = 40  # Exemple : 8h/jour * 5 jours
        return (heures_occupees / heures_totales) * 100 if heures_totales else 0

    # Représentation

    def __str__(self) -> str:
        if not self._seances:
            return "Aucune séance programmée."
        return "\n".join(str(s) for s in self._seances)
