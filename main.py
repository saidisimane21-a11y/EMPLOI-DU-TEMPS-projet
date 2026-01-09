import sys
from datetime import datetime
from PyQt6.QtWidgets import QApplication
from core.salle import Salle
from core.matiere import Matiere
from core.groupe import GroupeEtudiant
from core.creneau import Creneau
from core.enseignant import Enseignant
from core.seance import Seance
from core.emploi_du_temps import EmploiDuTemps
from users import Administrateur, EnseignantUser, Etudiant
from ui.main_window import MainWindow

# --- Création entités métier ---
salle1 = Salle(1, "Amphi 101", 100, "amphi", ["projecteur"])
salle2 = Salle(2, "TD 201", 30, "td", ["pc"])
groupe1 = GroupeEtudiant(1, "G1 Info", "Informatique", 30)
groupe2 = GroupeEtudiant(2, "G2 Info", "Informatique", 25)
matiere1 = Matiere("INFO101", "Algo", "cours", 2, ["projecteur"])
matiere2 = Matiere("INFO102", "BD", "cours", 2, ["pc"])

# Créneaux


def h(time_str):
    return datetime.strptime(time_str, "%H:%M").time()


creneau1 = Creneau("Lundi", h("08:00"), h("10:00"))
creneau2 = Creneau("Lundi", h("10:00"), h("12:00"))

# Enseignants
enseignant1 = Enseignant(1, "Dr. Dupont", [matiere1], [creneau1, creneau2])
enseignant2 = Enseignant(2, "Mme. Martin", [matiere2], [creneau1, creneau2])

# Séances
seance1 = Seance(matiere1, enseignant1, groupe1, salle1, creneau1)
seance2 = Seance(matiere2, enseignant2, groupe2, salle2, creneau2)

# Emploi du temps
edt = EmploiDuTemps()
edt.ajouter_seance(seance1)
edt.ajouter_seance(seance2)

# Utilisateurs (non utilisés pour PyQt ici, juste pour test)
admin = Administrateur("admin", "1234")
enseignant_user = EnseignantUser("dupont", "abcd", enseignant1)
etudiant_user = Etudiant("etu1", "pass", groupe1)

# --- Lancement PyQt ---
app = QApplication(sys.argv)
fenetre = MainWindow(edt, utilisateur=admin)
fenetre.show()
sys.exit(app.exec())

