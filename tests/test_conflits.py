from datetime import time
from core.creneau import Creneau
from core.salle import Salle
from core.groupe_etudiant import GroupeEtudiant
from core.matiere import Matiere
from core.enseignant import Enseignant
from core.seance import Seance
from services.conflict_detector import ConflictDetector


def test_conflit_salle():
    c = Creneau("Lundi", time(8, 0), time(10, 0))
    salle = Salle(1, "S1", 30, "td", [])
    groupe = GroupeEtudiant(1, "G1", "Info", 20)
    matiere = Matiere("M1", "Algo", "td", 2, [])
    ens = Enseignant(1, "Prof", [matiere], [c])

    s1 = Seance(matiere, ens, groupe, salle, c)
    s2 = Seance(matiere, ens, groupe, salle, c)

    conflits = ConflictDetector.detect(s1, s2)

    assert conflits
