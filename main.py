import sys
from datetime import datetime
from core.salle import Salle
from core.matiere import Matiere
from core.groupe_etudiant import GroupeEtudiant
from core.creneau import Creneau
from core.enseignant import Enseignant
from core.seance import Seance
from core.emploi_du_temps import EmploiDuTemps
from users.administrateur import Administrateur

# --- Création entités métier ---
salle1 = Salle(1, "Amphi 101", 100, "amphi", ["projecteur"])
salle2 = Salle(2, "TD 201", 30, "td", ["pc"])
groupe1 = GroupeEtudiant(1, "G1 Info", "Informatique", 30)
groupe2 = GroupeEtudiant(2, "G2 Info", "Informatique", 25)
matiere1 = Matiere("INFO101", "Algo", "cours", 2, ["projecteur"])
matiere2 = Matiere("INFO102", "BD", "cours", 2, ["pc"])

def h(time_str):
    return datetime.strptime(time_str, "%H:%M").time()

creneau1 = Creneau("Lundi", h("08:00"), h("10:00"))
creneau2 = Creneau("Lundi", h("10:00"), h("12:00"))

enseignant1 = Enseignant(1, "Dr. Dupont", [matiere1], [creneau1, creneau2])
enseignant2 = Enseignant(2, "Mme. Martin", [matiere2], [creneau1, creneau2])

seance1 = Seance(matiere1, enseignant1, groupe1, salle1, creneau1)
seance2 = Seance(matiere2, enseignant2, groupe2, salle2, creneau2)

edt = EmploiDuTemps()
edt.ajouter_seance(seance1)
edt.ajouter_seance(seance2)

# Utilisateur admin minimal pour test back-end
admin = Administrateur("admin", "1234")

# On ne lance pas PyQt, juste vérifier que tout compile
print("Back-end métier prêt, EDT contient ces séances :")
for s in edt.seances:
    print(s)
