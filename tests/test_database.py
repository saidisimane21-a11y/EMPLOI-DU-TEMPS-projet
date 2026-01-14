from core.salle import Salle
from core.enseignant import Enseignant
from core.creneau import Creneau
from core.seance import Seance
import data.database_manager as db
from datetime import time

# --------------------
# 1. Initialiser la base (une seule fois)
# --------------------
db.initialiser_base()

# --------------------
# 2. Créer des salles et enseignants
# --------------------
# Créneaux de disponibilités
cr1 = Creneau("lundi", time(8, 0), time(10, 0))
cr2 = Creneau("mardi", time(14, 0), time(16, 0))

# Salle avec disponibilités
salle1 = Salle(1, "Amphi A", 100, "amphi", disponibilites=[cr1])
salle2 = Salle(2, "TD B", 30, "td")
salle2.ajouter_disponibilite(cr2)

# Enseignants avec disponibilités
ens1 = Enseignant(1, "Mme Dupont", disponibilites=[cr1])
ens2 = Enseignant(2, "M. Martin")
ens2.ajouter_disponibilite(cr2)

# --------------------
# 3. Sauvegarder dans la DB
# --------------------
db.sauvegarder_salle(salle1)
db.sauvegarder_salle(salle2)

db.sauvegarder_enseignant(ens1)
db.sauvegarder_enseignant(ens2)

# --------------------
# 4. Charger depuis la DB
# --------------------
salles = db.charger_salles()
enseignants = db.charger_enseignants()

print("Salles chargées :")
for s in salles:
    print(f"{s} -> dispo: {[str(d) for d in s.disponibilites]}")

print("\nEnseignants chargés :")
for e in enseignants:
    print(f"{e} -> dispo: {[str(d) for d in e.disponibilites]}")

# --------------------
# 5. Créer et sauvegarder une séance
# --------------------
# Choisir un créneau pour la séance
cr_seance = Creneau("lundi", time(8, 0), time(9, 30))
seance1 = Seance(salles[0], enseignants[0], None,
                 cr_seance)  # groupe None pour test
db.sauvegarder_seance(seance1)

# Charger les séances
seances = db.charger_seances(salles, enseignants)
print("\nSéances chargées :")
for s in seances:
    print(
        f"Salle: {s.salle.nom}, Enseignant: {s.enseignant.nom}, Créneau: {s.creneau}")
