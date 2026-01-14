from core.emploi_du_temps import EmploiDuTemps
from core.seance import Seance
from core.creneau import Creneau
from core.salle import Salle
from core.enseignant import Enseignant
from core.groupe_etudiant import GroupeEtudiant
from datetime import time
from core.matiere import Matiere

def test_ajout_seance_sans_conflit():
    edt = EmploiDuTemps()
    salle = Salle(1, "TD1", 30, "td")
    ens = Enseignant(1, "Prof A")
    grp = GroupeEtudiant(1, "GI1", "Info", 30)
    matiere = Matiere("MATH1", "Math", "td", 2, [])

    c = Creneau("mercredi", time(8, 0), time(10, 0))
    s = Seance(matiere=matiere, enseignant=ens, groupe=grp, salle=salle, creneau=c)

    edt.ajouter_seance(s)
    assert len(edt.seances) == 1
