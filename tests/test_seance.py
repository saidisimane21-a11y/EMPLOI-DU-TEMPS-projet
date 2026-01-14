# tests/test_seance.py
from datetime import time
import pytest
from core.creneau import Creneau
from core.salle import Salle
from core.groupe_etudiant import GroupeEtudiant
from core.seance import Seance
from users.enseignant_user import Enseignant


def test_creation_seance():
    # Création d'un créneau
    cr = Creneau("lundi", time(8, 0), time(10, 0))

    # Création des objets nécessaires
    salle = Salle(1, "Amphi A", 100, "amphi", disponibilites=[cr])
    enseignant = Enseignant(1, "Mme Dupont", disponibilites=[cr])
    groupe = GroupeEtudiant(1, "Groupe 1")

    # Création de la séance
    seance = Seance(salle, enseignant, groupe, cr)

    # Vérifications
    assert seance.salle == salle
    assert seance.enseignant == enseignant
    assert seance.groupe == groupe
    assert seance.creneau == cr


def test_conflit_seance():
    cr = Creneau("lundi", time(8, 0), time(10, 0))

    salle = Salle(1, "Amphi A", 100, "amphi", disponibilites=[cr])
    enseignant = Enseignant(1, "Mme Dupont", disponibilites=[cr])
    groupe = GroupeEtudiant(1, "Groupe 1")

    seance1 = Seance(salle, enseignant, groupe, cr)
    seance2 = Seance(salle, enseignant, groupe, cr)

    # Conflit détecté par comparaison simple
    assert seance1.creneau == seance2.creneau
    assert seance1.salle == seance2.salle
