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
from ui.main_window import MainWindow
from ui.login_window import LoginWindow
from database.base import get_session, init_db
from database.repository import SeanceRepository, EnseignantRepository
from users.administrateur import Administrateur
from users.enseignant_user import EnseignantUser
from users.etudiant import Etudiant

# Fix encoding for Windows console
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def init_data():
    """Charge les données depuis la base de données."""
    init_db()  # Assure que les tables existent
    session = next(get_session())
    try:
        edt = EmploiDuTemps()
        # Charger les séances depuis la DB
        seances = SeanceRepository.get_all_domain(session)
        for s in seances:
            edt._seances.append(s) # Direct append to bypass conflict check on load if needed
        return edt
    finally:
        session.close()


def main():
    """Point d'entrée principal de l'application."""
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
    # Étape 1: Connexion
    login_dialog = LoginWindow()
    if login_dialog.exec() != LoginWindow.Accepted:
        sys.exit(0)
        
    db_user = login_dialog.user
    
    # Étape 2: Initialiser les données de l'EDT
    edt = init_data()
    
    # Étape 3: Créer l'objet utilisateur domaine selon le rôle
    role = db_user.role
    if role == "admin":
        user = Administrateur(db_user.username, "********", db_user.id, edt)
    elif role == "enseignant":
        # Trouver l'entité Enseignant correspondante (par nom ou ID si lié)
        session = next(get_session())
        # On suppose que nom_complet de l'utilisateur correspond au nom de l'enseignant
        from database.models import EnseignantModel
        db_enseig = session.query(EnseignantModel).filter_by(nom=db_user.nom_complet).first()
        if db_enseig:
            enseig_domain = EnseignantRepository.get_by_id_domain(session, db_enseig.id)
        else:
            # Fallback if not found
            enseig_domain = Enseignant(1, db_user.nom_complet, [], [])
        user = EnseignantUser(db_user.username, "********", db_user.id, enseig_domain)
        session.close()
    else: # etudiant
        # L'import de GroupeEtudiant est nécessaire si on veut créer un objet groupe
        from core.groupe_etudiant import GroupeEtudiant
        groupe_dummy = GroupeEtudiant(1, "G1", "Informatique", 30)
        user = Etudiant(db_user.username, "********", db_user.id, groupe_dummy)
        
    # Étape 4: Lancer l'interface principale
    window = MainWindow(edt, user)
    window.show()
    
    print(f"✅ Application lancée pour {db_user.username} ({role})")
    print(f"📊 {len(edt.seances)} séances chargées")
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
