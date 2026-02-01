"""Seed database with initial test data."""

from database.base import get_session, init_db
from database.repository import (
    SalleRepository, MatiereRepository, GroupeEtudiantRepository,
    UtilisateurRepository, EnseignantRepository, SeanceRepository,
    CreneauRepository
)
from data.testDatat import obtenir_tout_le_jeu_de_donnees


def seed_database():
    """Seed the database with test data."""
    # Initialize database
    init_db()
    
    # Get test data
    data = obtenir_tout_le_jeu_de_donnees()
    
    session = next(get_session())
    
    try:
        # Seed salles
        print("[Salles] Seeding salles...")
        from database.models import SalleModel, MatiereModel, GroupeEtudiantModel, EnseignantModel, UtilisateurModel
        for salle in data['salles']:
            if not session.query(SalleModel).filter_by(id=salle.id).first():
                SalleRepository.create(session, salle)
        
        # Seed matieres
        print("[Matieres] Seeding matieres...")
        for matiere in data['matieres']:
            if not session.query(MatiereModel).filter_by(code=matiere.code).first():
                MatiereRepository.create(session, matiere)
        
        # Seed groupes
        print("[Groupes] Seeding groupes...")
        for groupe in data['groupes']:
            if not session.query(GroupeEtudiantModel).filter_by(id=groupe.id).first():
                GroupeEtudiantRepository.create(session, groupe)

        # Seed enseignants
        print("[Enseignants] Seeding enseignants...")
        for enseignant in data['enseignants']:
            if not session.query(EnseignantModel).filter_by(id=enseignant.id).first():
                EnseignantRepository.create(session, enseignant)
        
        # Create default users
        print("[Users] Creating default users...")
        if not session.query(UtilisateurModel).filter_by(username="admin").first():
            UtilisateurRepository.create_user(
                session, 
                username="admin",
                password="admin123",
                role="admin",
                email="admin@emploi.com",
                nom_complet="Administrateur"
            )
        
        if not session.query(UtilisateurModel).filter_by(username="prof").first():
            UtilisateurRepository.create_user(
                session,
                username="prof",
                password="prof123",
                role="enseignant",
                email="prof@emploi.com",
                nom_complet="Professeur Test"
            )
        
        if not session.query(UtilisateurModel).filter_by(username="etudiant").first():
            UtilisateurRepository.create_user(
                session,
                username="etudiant",
                password="etudiant123",
                role="etudiant",
                email="etudiant@emploi.com",
                nom_complet="Étudiant Test"
            )
        
        # Seed seances
        print("[Seances] Seeding seances...")
        from database.models import SalleModel, MatiereModel, GroupeEtudiantModel, EnseignantModel
        for seance in data['seances']:
            # Find DB IDs
            db_salle = session.query(SalleModel).filter_by(nom=seance.salle.nom).first()
            db_matiere = session.query(MatiereModel).filter_by(code=seance.matiere.code).first()
            db_groupe = session.query(GroupeEtudiantModel).filter_by(nom=seance.groupe.nom).first()
            db_enseig = session.query(EnseignantModel).filter_by(nom=seance.enseignant.nom).first()
            db_creneau = CreneauRepository.get_or_create(session, seance.creneau)
            
            SeanceRepository.create(
                session, seance, 
                db_matiere.id, db_enseig.id, db_groupe.id, db_salle.id, db_creneau.id
            )
            
        session.commit()
        print("[OK] Database seeded successfully!")
        
        print("\n[Summary] Summary:")
        print(f"  - {len(data['salles'])} salles")
        print(f"  - {len(data['matieres'])} matières")
        print(f"  - {len(data['groupes'])} groupes")
        print(f"  - 3 utilisateurs")
        print(f"\n[Auth] Default credentials:")
        print(f"  Admin: admin/admin123")
        print(f"  Prof: prof/prof123")
        print(f"  Étudiant: etudiant/etudiant123")
        
    except Exception as e:
        session.rollback()
        print(f"[Error] Error seeding database: {e}")
        raise
    finally:
        session.close()


if __name__ == "__main__":
    seed_database()
