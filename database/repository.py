"""Repository pattern for database operations."""

from typing import List, Optional
from sqlalchemy.orm import Session
from database.models import (
    SalleModel, MatiereModel, GroupeEtudiantModel,
    CreneauModel, EnseignantModel, SeanceModel,
    UtilisateurModel, ReservationModel
)
from core.salle import Salle
from core.matiere import Matiere
from core.groupe_etudiant import GroupeEtudiant
from core.creneau import Creneau
from core.enseignant import Enseignant
from core.seance import Seance
from core.reservation import Reservation
import bcrypt


class SalleRepository:
    """Repository for Salle operations."""
    
    @staticmethod
    def create(session: Session, salle: Salle) -> SalleModel:
        """Create a new salle in database."""
        db_salle = SalleModel(
            id=salle.id,
            nom=salle.nom,
            capacite=salle.capacite,
            type_salle=salle.type,
            equipements=list(salle.equipements)
        )
        session.add(db_salle)
        session.flush()
        return db_salle
    
    @staticmethod
    def get_all(session: Session) -> List[Salle]:
        """Get all salles from database."""
        db_salles = session.query(SalleModel).all()
        return [
            Salle(s.id, s.nom, s.capacite, s.type_salle, s.equipements)
            for s in db_salles
        ]
    
    @staticmethod
    def get_by_id(session: Session, salle_id: int) -> Optional[Salle]:
        """Get a salle by ID."""
        db_salle = session.query(SalleModel).filter(SalleModel.id == salle_id).first()
        if db_salle:
            return Salle(db_salle.id, db_salle.nom, db_salle.capacite, 
                        db_salle.type_salle, db_salle.equipements)
        return None


class MatiereRepository:
    """Repository for Matiere operations."""
    
    @staticmethod
    def create(session: Session, matiere: Matiere) -> MatiereModel:
        """Create a new matiere in database."""
        db_matiere = MatiereModel(
            code=matiere.code,
            nom=matiere.nom,
            type_cours=matiere.type_seance,
            heures_par_semaine=matiere.volume_horaire,
            equipements_requis=list(matiere.equipements_requis)
        )
        session.add(db_matiere)
        session.flush()
        return db_matiere
    
    @staticmethod
    def get_all(session: Session) -> List[Matiere]:
        """Get all matieres from database."""
        db_matieres = session.query(MatiereModel).all()
        return [
            Matiere(m.code, m.nom, m.type_cours, m.heures_par_semaine, m.equipements_requis)
            for m in db_matieres
        ]


    @staticmethod
    def get_by_code(session: Session, code: str) -> Optional[Matiere]:
        """Get a matiere by its code."""
        db_matiere = session.query(MatiereModel).filter(MatiereModel.code == code).first()
        if db_matiere:
            return Matiere(db_matiere.code, db_matiere.nom, db_matiere.type_cours, 
                          db_matiere.heures_par_semaine, db_matiere.equipements_requis)
        return None


class GroupeEtudiantRepository:
    """Repository for GroupeEtudiant operations."""
    
    @staticmethod
    def create(session: Session, groupe: GroupeEtudiant) -> GroupeEtudiantModel:
        """Create a new groupe in database."""
        db_groupe = GroupeEtudiantModel(
            id=groupe.id,
            nom=groupe.nom,
            filiere=groupe.filiere,
            effectif=groupe.effectif,
            niveau=groupe.niveau
        )
        session.add(db_groupe)
        session.flush()
        return db_groupe
    
    @staticmethod
    def get_all(session: Session) -> List[GroupeEtudiant]:
        """Get all groupes from database."""
        db_groupes = session.query(GroupeEtudiantModel).all()
        return [
            GroupeEtudiant(g.id, g.nom, g.filiere, g.effectif, g.niveau)
            for g in db_groupes
        ]


class CreneauRepository:
    """Repository for Creneau operations."""
    
    @staticmethod
    def create(session: Session, creneau: Creneau) -> CreneauModel:
        """Create a new creneau in database."""
        db_creneau = CreneauModel(
            jour=creneau.jour,
            heure_debut=creneau.heure_debut,
            heure_fin=creneau.heure_fin
        )
        session.add(db_creneau)
        session.flush()
        return db_creneau
    
    @staticmethod
    def get_all(session: Session) -> List[Creneau]:
        """Get all creneaux from database."""
        db_creneaux = session.query(CreneauModel).all()
        return [
            Creneau(c.jour, c.heure_debut, c.heure_fin)
            for c in db_creneaux
        ]
    
    @staticmethod
    def get_or_create(session: Session, creneau: Creneau) -> CreneauModel:
        """Get an existing creneau or create a new one."""
        db_creneau = session.query(CreneauModel).filter(
            CreneauModel.jour == creneau.jour,
            CreneauModel.heure_debut == creneau.heure_debut,
            CreneauModel.heure_fin == creneau.heure_fin
        ).first()
        
        if not db_creneau:
            db_creneau = CreneauModel(
                jour=creneau.jour,
                heure_debut=creneau.heure_debut,
                heure_fin=creneau.heure_fin
            )
            session.add(db_creneau)
            session.flush()
        return db_creneau


class EnseignantRepository:
    """Repository for Enseignant operations."""
    
    @staticmethod
    def create(session: Session, enseignant: Enseignant) -> EnseignantModel:
        """Create a new enseignant in database with matieres and disponibilites."""
        db_enseignant = EnseignantModel(
            id=enseignant.id,
            nom=enseignant.nom
        )
        
        # Link matieres
        for matiere in enseignant.matieres:
            db_matiere = session.query(MatiereModel).filter(MatiereModel.code == matiere.code).first()
            if db_matiere:
                db_enseignant.matieres.append(db_matiere)
        
        # Link or create disponibilites
        for dispo in enseignant.disponibilites:
            db_creneau = CreneauRepository.get_or_create(session, dispo)
            db_enseignant.disponibilites.append(db_creneau)
            
        session.add(db_enseignant)
        session.flush()
        return db_enseignant
    
    @staticmethod
    def get_all(session: Session) -> List[Enseignant]:
        """Get all enseignants from database."""
        db_enseignants = session.query(EnseignantModel).all()
        result = []
        for e in db_enseignants:
            matieres = [
                Matiere(m.code, m.nom, m.type_cours, m.heures_par_semaine, m.equipements_requis)
                for m in e.matieres
            ]
            dispos = [
                Creneau(c.jour, c.heure_debut, c.heure_fin)
                for c in e.disponibilites
            ]
            result.append(Enseignant(e.id, e.nom, matieres, dispos))
        return result

    @staticmethod
    def get_by_id_domain(session: Session, enseignant_id: int) -> Optional[Enseignant]:
        """Get an enseignant by ID and return domain object."""
        e = session.query(EnseignantModel).filter(EnseignantModel.id == enseignant_id).first()
        if not e:
            return None
        matieres = [
            Matiere(m.code, m.nom, m.type_cours, m.heures_par_semaine, m.equipements_requis)
            for m in e.matieres
        ]
        dispos = [
            Creneau(c.jour, c.heure_debut, c.heure_fin)
            for c in e.disponibilites
        ]
        return Enseignant(e.id, e.nom, matieres, dispos)


class UtilisateurRepository:
    """Repository for Utilisateur operations."""
    
    @staticmethod
    def create_user(session: Session, username: str, password: str, role: str, 
                   email: str = None, nom_complet: str = None) -> UtilisateurModel:
        """Create a new user with hashed password."""
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        db_user = UtilisateurModel(
            username=username,
            password_hash=password_hash,
            role=role,
            email=email,
            nom_complet=nom_complet
        )
        session.add(db_user)
        session.flush()
        return db_user
    
    @staticmethod
    def verify_password(password: str, password_hash: str) -> bool:
        """Verify a password against its hash."""
        return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))
    
    @staticmethod
    def get_by_username(session: Session, username: str) -> Optional[UtilisateurModel]:
        """Get user by username."""
        return session.query(UtilisateurModel).filter(
            UtilisateurModel.username == username
        ).first()
    
    @staticmethod
    def authenticate(session: Session, username: str, password: str) -> Optional[UtilisateurModel]:
        """Authenticate a user."""
        user = UtilisateurRepository.get_by_username(session, username)
        if user and UtilisateurRepository.verify_password(password, user.password_hash):
            return user
        return None


class SeanceRepository:
    """Repository for Seance operations."""
    
    @staticmethod
    def create(session: Session, seance: Seance, 
              matiere_id: int, enseignant_id: int, groupe_id: int,
              salle_id: int, creneau_id: int) -> SeanceModel:
        """Create a new seance in database."""
        db_seance = SeanceModel(
            matiere_id=matiere_id,
            enseignant_id=enseignant_id,
            groupe_id=groupe_id,
            salle_id=salle_id,
            creneau_id=creneau_id
        )
        session.add(db_seance)
        session.flush()
        return db_seance
    
    @staticmethod
    def get_all(session: Session) -> List[SeanceModel]:
        """Get all seances with relationships loaded."""
        return session.query(SeanceModel).all()

    @staticmethod
    def get_all_domain(session: Session) -> List[Seance]:
        """Get all seances as domain objects."""
        db_seances = session.query(SeanceModel).all()
        domain_seances = []
        for s in db_seances:
            matiere = Matiere(s.matiere.code, s.matiere.nom, s.matiere.type_cours, 
                             s.matiere.heures_par_semaine, s.matiere.equipements_requis)
            enseignant = Enseignant(s.enseignant.id, s.enseignant.nom, [], []) # Detail loading if needed
            # For simplicity, we just need names for the dashboard in some cases,
            # but for full domain objects we'd need to reconstruct them properly.
            # Let's do it properly:
            enseignant = EnseignantRepository.get_by_id_domain(session, s.enseignant_id)
            groupe = GroupeEtudiant(s.groupe.id, s.groupe.nom, s.groupe.filiere, 
                                   s.groupe.effectif, s.groupe.niveau)
            salle = Salle(s.salle.id, s.salle.nom, s.salle.capacite, 
                         s.salle.type_salle, s.salle.equipements)
            creneau = Creneau(s.creneau.jour, s.creneau.heure_debut, s.creneau.heure_fin)
            
            domain_seances.append(Seance(matiere, enseignant, groupe, salle, creneau))
        return domain_seances

    @staticmethod
    def delete(session: Session, seance_id: int) -> bool:
        """Delete a seance by ID."""
        db_seance = session.query(SeanceModel).filter(SeanceModel.id == seance_id).first()
        if db_seance:
            session.delete(db_seance)
            return True
        return False

    @staticmethod
    def delete_by_details(session: Session, seance: Seance) -> bool:
        """Find and delete a seance based on its domain attributes."""
        # Find the seance in DB that matches all core attributes
        # This is a bit complex due to relations, but let's try a direct query
        db_seance = session.query(SeanceModel).join(MatiereModel).join(EnseignantModel).join(GroupeEtudiantModel).join(SalleModel).join(CreneauModel).filter(
            MatiereModel.code == seance.matiere.code,
            EnseignantModel.nom == seance.enseignant.nom,
            GroupeEtudiantModel.nom == seance.groupe.nom,
            SalleModel.nom == seance.salle.nom,
            CreneauModel.jour == seance.creneau.jour,
            CreneauModel.heure_debut == seance.creneau.heure_debut,
            CreneauModel.heure_fin == seance.creneau.heure_fin
        ).first()
        
        if db_seance:
            session.delete(db_seance)
            session.commit()
            return True
        return False


class ReservationRepository:
    """Repository for Reservation operations."""
    
    @staticmethod
    def create(session: Session, reservation: Reservation, utilisateur_id: int) -> ReservationModel:
        """Create a new reservation in database."""
        # Get or create creneau
        db_creneau = CreneauRepository.get_or_create(session, reservation.creneau)
        
        # Get salle
        db_salle = session.query(SalleModel).filter(SalleModel.nom == reservation.salle.nom).first()
        if not db_salle:
            raise ValueError(f"Salle {reservation.salle.nom} non trouvée.")

        db_reservation = ReservationModel(
            utilisateur_id=utilisateur_id,
            salle_id=db_salle.id,
            creneau_id=db_creneau.id,
            motif=reservation.motif,
            statut='en_attente'
        )
        session.add(db_reservation)
        session.commit()
        return db_reservation

    @staticmethod
    def get_by_user(session: Session, utilisateur_id: int) -> List[ReservationModel]:
        """Get all reservations for a specific user."""
        return session.query(ReservationModel).filter(
            ReservationModel.utilisateur_id == utilisateur_id
        ).all()

    @staticmethod
    def get_all(session: Session) -> List[ReservationModel]:
        """Get all reservations (for admin)."""
        return session.query(ReservationModel).all()

    @staticmethod
    def update_status(session: Session, reservation_id: int, status: str) -> bool:
        """Update reservation status."""
        db_res = session.query(ReservationModel).filter(ReservationModel.id == reservation_id).first()
        if db_res:
            db_res.statut = status
            session.commit()
            return True
        return False
