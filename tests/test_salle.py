from core.salle import Salle
from core.creneau import Creneau
from datetime import time

def test_salle_disponible():
    c1 = Creneau("lundi", time(8, 0), time(10, 0))
    salle = Salle(1, "TD1", 30, "td")
    salle.ajouter_disponibilite(c1)

    c_test = Creneau("lundi", time(10, 0), time(12, 0))
    assert salle.est_disponible(c_test)
