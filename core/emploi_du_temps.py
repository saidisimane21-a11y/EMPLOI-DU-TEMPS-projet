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
        conflit = self.verifier_conflit(nouvelle_seance)
        if conflit:
            raise ValueError(f"Conflit détecté : {conflit}")
        self._seances.append(nouvelle_seance)

    def verifier_conflit(self, s: Seance) -> str:
        """
        Vérifie si une séance entre en conflit avec les séances existantes.
        Retourne une chaîne décrivant le conflit, ou None si pas de conflit.
        """
        for existante in self._seances:
            if existante.creneau == s.creneau:
                if existante.salle == s.salle:
                    return f"La salle '{s.salle.nom}' est déjà occupée."
                if existante.enseignant == s.enseignant:
                    return f"L'enseignant '{s.enseignant.nom}' a déjà un cours sur ce créneau."
                if existante.groupe == s.groupe:
                    return f"Le groupe '{s.groupe.nom}' a déjà un cours sur ce créneau."
        return None
    
    def supprimer_seance(self, seance: Seance) -> None:
        """
        Supprime une séance de l'emploi du temps.
        """
        if seance in self._seances:
            self._seances.remove(seance)
        else:
            raise ValueError("La séance spécifiée n'existe pas dans l'emploi du temps.")

  

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
