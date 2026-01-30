# -*- coding: utf-8 -*-
import sys
import io
from datetime import datetime
from PySide6.QtWidgets import QApplication
from core.salle import Salle
from core.matiere import Matiere
from core.groupe_etudiant import GroupeEtudiant
from core.creneau import Creneau
from core.enseignant import Enseignant
from core.seance import Seance
from core.emploi_du_temps import EmploiDuTemps
from users.administrateur import Administrateur
from ui.main_window import MainWindow

# Fix encoding for Windows console
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def init_data():
    """Initialise les données de démonstration."""
    # --- Création entités métier ---
    salle1 = Salle(1, "Amphi 101", 100, "amphi", ["projecteur"])
    salle2 = Salle(2, "TD 201", 30, "td", ["pc"])
    salle3 = Salle(3, "TP 301", 30, "tp", ["pc", "réseau"])  # Capacité augmentée à 30
    
    groupe1 = GroupeEtudiant(1, "G1 Info", "Informatique", 30)
    groupe2 = GroupeEtudiant(2, "G2 Info", "Informatique", 25)
    
    matiere1 = Matiere("INFO101", "Algorithmique", "cours", 2, ["projecteur"])
    matiere2 = Matiere("INFO102", "Base de Données", "cours", 2, ["pc"])
    matiere3 = Matiere("INFO103", "Réseaux", "tp", 2, ["pc", "réseau"])
    
    def h(time_str):
        return datetime.strptime(time_str, "%H:%M").time()
    
    # Créneaux variés
    creneau1 = Creneau("Lundi", h("08:00"), h("10:00"))
    creneau2 = Creneau("Lundi", h("10:00"), h("12:00"))
    creneau3 = Creneau("Mardi", h("14:00"), h("16:00"))
    creneau4 = Creneau("Mercredi", h("08:00"), h("10:00"))
    creneau5 = Creneau("Jeudi", h("10:00"), h("12:00"))
    
    enseignant1 = Enseignant(1, "Dr. Dupont", [matiere1], [creneau1, creneau4])
    enseignant2 = Enseignant(2, "Mme. Martin", [matiere2], [creneau2, creneau5])
    enseignant3 = Enseignant(3, "M. Bernard", [matiere3], [creneau3])
    
    # Créer l'emploi du temps
    edt = EmploiDuTemps()
    
    # Ajouter plusieurs séances
    seances = [
        Seance(matiere1, enseignant1, groupe1, salle1, creneau1),
        Seance(matiere2, enseignant2, groupe2, salle2, creneau2),
        Seance(matiere3, enseignant3, groupe1, salle3, creneau3),
        Seance(matiere1, enseignant1, groupe2, salle1, creneau4),
        Seance(matiere2, enseignant2, groupe1, salle2, creneau5),
    ]
    
    for seance in seances:
        try:
            edt.ajouter_seance(seance)
        except ValueError as e:
            print(f"⚠️ Conflit détecté: {e}")
    
    return edt


def main():
    """Point d'entrée principal de l'application."""
    # Créer l'application Qt
    app = QApplication(sys.argv)
    
    # Style de l'application
    app.setStyle("Fusion")
    
    # Initialiser les données
    edt = init_data()
    
    # Créer un utilisateur administrateur (avec l'emploi du temps)
    admin = Administrateur("admin", "1234", edt)
    
    # Créer et afficher la fenêtre principale
    window = MainWindow(edt, admin)
    window.show()
    
    print("✅ Application d'emploi du temps lancée!")
    print(f"📊 {len(edt.seances)} séances chargées")
    
    # Lancer la boucle d'événements
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
