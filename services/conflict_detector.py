from services.constraints import ConflictType

class ConflictDetector:
    """
    Responsable de la détection des conflits
    entre deux séances.
    """

    @staticmethod
    def creneaux_se_chevauchent(c1, c2) -> bool:
        if c1.jour != c2.jour:
            return False

        return not (
            c1.heure_fin <= c2.heure_debut
            or c2.heure_fin <= c1.heure_debut
        )

    @staticmethod
    def detect(seance1, seance2):
        conflits = []

        if ConflictDetector.creneaux_se_chevauchent(
            seance1.creneau, seance2.creneau
        ):
            if seance1.salle == seance2.salle:
                conflits.append(ConflictType.SALLE)

            if seance1.enseignant == seance2.enseignant:
                conflits.append(ConflictType.ENSEIGNANT)

            if seance1.groupe == seance2.groupe:
                conflits.append(ConflictType.GROUPE)

        return conflits
