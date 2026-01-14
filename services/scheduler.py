class Scheduler:
    """
    Responsable de la génération automatique
    de l'emploi du temps (à venir).
    """
from services.conflict_detector import ConflictDetector
from core.seance import Seance


class Scheduler:
    """
    Génération automatique de l'emploi du temps
    avec un algorithme glouton.
    """

    def __init__(self, salles, creneaux):
        self.salles = salles
        self.creneaux = creneaux

    def generer(self, emploi_du_temps, demandes):
        """
        demandes : liste de tuples (matiere, enseignant, groupe)
        """
        for matiere, enseignant, groupe in demandes:
            seance_placee = False

            for creneau in self.creneaux:
                for salle in self.salles:
                    # Vérifier compatibilité salle / matière
                    if not salle.est_compatible(groupe.effectif, matiere.equipements_requis):
                        continue

                    # Vérifier disponibilité enseignant
                    if creneau not in enseignant.disponibilites:
                        continue

                    nouvelle_seance = Seance(
                        matiere,
                        enseignant,
                        groupe,
                        salle,
                        creneau
                    )

                    if not self._a_conflit(nouvelle_seance, emploi_du_temps.seances):
                        emploi_du_temps.ajouter_seance(nouvelle_seance)
                        seance_placee = True
                        break

                if seance_placee:
                    break

            if not seance_placee:
                raise Exception(
                    f"Aucune solution trouvée pour {matiere.nom}"
                )

    def _a_conflit(self, nouvelle_seance, seances_existantes):
        for seance in seances_existantes:
            conflits = ConflictDetector.detect(
                nouvelle_seance, seance
            )
            if conflits:
                return True
        return False

