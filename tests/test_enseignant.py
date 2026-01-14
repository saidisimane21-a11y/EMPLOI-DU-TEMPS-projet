from core.enseignant import Enseignant
from core.creneau import Creneau
from datetime import time

def test_enseignant_disponible():
    c = Creneau("mardi", time(14, 0), time(16, 0))
    e = Enseignant(1, "Prof A", disponibilites=[c])

    assert e.est_disponible(c)
