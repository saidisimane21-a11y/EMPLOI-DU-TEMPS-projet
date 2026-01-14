from datetime import time
from core.creneau import Creneau
from core.salle import Salle
from core.groupe_etudiant import GroupeEtudiant
from core.matiere import Matiere
from core.enseignant import Enseignant
from core.emploi_du_temps import EmploiDuTemps
from services.scheduler import Scheduler


def test_scheduler_simple():
    c1 = Creneau("Lundi", time(8, 0), time(10, 0))
    salle = Salle(1, "S1", 40, "td", [])
    groupe = GroupeEtudiant(1, "G1", "Info", 30)
    matiere = Matiere("M1", "Algo", "cours", 2, [])
    ens = Enseignant(1, "Prof", [matiere], [c1])

    edt = EmploiDuTemps()
    scheduler = Scheduler([salle], [c1])

    scheduler.generer(
        edt,
        demandes=[(matiere, ens, groupe)]
    )

    assert len(edt.seances) == 1
