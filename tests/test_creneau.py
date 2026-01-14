from datetime import time
from core.creneau import Creneau


def test_creation_creneau():
    c = Creneau("lundi", time(8, 0), time(10, 0))
    assert c.jour == "lundi"
    assert c.heure_debut < c.heure_fin
    print("Test creation_creneau passé !")


test_creation_creneau()
