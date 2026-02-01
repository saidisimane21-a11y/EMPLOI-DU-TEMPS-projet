"""SQLAlchemy models for database persistence."""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table, Time, Boolean, JSON
from sqlalchemy.orm import relationship
from database.base import Base
from datetime import datetime


# Association tables for many-to-many relationships
enseignant_matiere = Table(
    'enseignant_matiere',
    Base.metadata,
    Column('enseignant_id', Integer, ForeignKey('enseignants.id')),
    Column('matiere_id', Integer, ForeignKey('matieres.id'))
)

enseignant_disponibilite = Table(
    'enseignant_disponibilite',
    Base.metadata,
    Column('enseignant_id', Integer, ForeignKey('enseignants.id')),
    Column('creneau_id', Integer, ForeignKey('creneaux.id'))
)


class SalleModel(Base):
    """Database model for Salle (Classroom)."""
    __tablename__ = 'salles'
    
    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(100), nullable=False, unique=True)
    capacite = Column(Integer, nullable=False)
    type_salle = Column(String(50), nullable=False)  # amphi, td, tp, labo
    equipements = Column(JSON, default=list)  # Liste d'équipements
    
    # Relationships
    seances = relationship("SeanceModel", back_populates="salle")
    reservations = relationship("ReservationModel", back_populates="salle")
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class MatiereModel(Base):
    """Database model for Matiere (Subject)."""
    __tablename__ = 'matieres'
    
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(50), nullable=False, unique=True)
    nom = Column(String(200), nullable=False)
    type_cours = Column(String(50), nullable=False)  # cours, td, tp
    heures_par_semaine = Column(Integer, default=2)
    equipements_requis = Column(JSON, default=list)
    
    # Relationships
    seances = relationship("SeanceModel", back_populates="matiere")
    enseignants = relationship("EnseignantModel", secondary=enseignant_matiere, back_populates="matieres")
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class GroupeEtudiantModel(Base):
    """Database model for GroupeEtudiant (Student Group)."""
    __tablename__ = 'groupes_etudiants'
    
    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(100), nullable=False, unique=True)
    filiere = Column(String(100), nullable=False)
    effectif = Column(Integer, nullable=False)
    niveau = Column(String(50), nullable=True)  # L1, L2, L3, M1, M2, etc.
    
    # Relationships
    seances = relationship("SeanceModel", back_populates="groupe")
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class CreneauModel(Base):
    """Database model for Creneau (Time Slot)."""
    __tablename__ = 'creneaux'
    
    id = Column(Integer, primary_key=True, index=True)
    jour = Column(String(20), nullable=False)  # Lundi, Mardi, etc.
    heure_debut = Column(Time, nullable=False)
    heure_fin = Column(Time, nullable=False)
    
    # Relationships
    seances = relationship("SeanceModel", back_populates="creneau")
    enseignants = relationship("EnseignantModel", secondary=enseignant_disponibilite, back_populates="disponibilites")
    
    created_at = Column(DateTime, default=datetime.utcnow)


class EnseignantModel(Base):
    """Database model for Enseignant (Teacher)."""
    __tablename__ = 'enseignants'
    
    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(200), nullable=False)
    email = Column(String(200), unique=True, nullable=True)
    
    # Relationships
    matieres = relationship("MatiereModel", secondary=enseignant_matiere, back_populates="enseignants")
    disponibilites = relationship("CreneauModel", secondary=enseignant_disponibilite, back_populates="enseignants")
    seances = relationship("SeanceModel", back_populates="enseignant")
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class SeanceModel(Base):
    """Database model for Seance (Class Session)."""
    __tablename__ = 'seances'
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign keys
    matiere_id = Column(Integer, ForeignKey('matieres.id'), nullable=False)
    enseignant_id = Column(Integer, ForeignKey('enseignants.id'), nullable=False)
    groupe_id = Column(Integer, ForeignKey('groupes_etudiants.id'), nullable=False)
    salle_id = Column(Integer, ForeignKey('salles.id'), nullable=False)
    creneau_id = Column(Integer, ForeignKey('creneaux.id'), nullable=False)
    
    # Relationships
    matiere = relationship("MatiereModel", back_populates="seances")
    enseignant = relationship("EnseignantModel", back_populates="seances")
    groupe = relationship("GroupeEtudiantModel", back_populates="seances")
    salle = relationship("SalleModel", back_populates="seances")
    creneau = relationship("CreneauModel", back_populates="seances")
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class UtilisateurModel(Base):
    """Database model for Utilisateur (User)."""
    __tablename__ = 'utilisateurs'
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False)  # admin, enseignant, etudiant
    email = Column(String(200), unique=True, nullable=True)
    nom_complet = Column(String(200), nullable=True)
    
    # Relationships
    reservations = relationship("ReservationModel", back_populates="utilisateur")
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ReservationModel(Base):
    """Database model for Reservation (Room Booking)."""
    __tablename__ = 'reservations'
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign keys
    utilisateur_id = Column(Integer, ForeignKey('utilisateurs.id'), nullable=False)
    salle_id = Column(Integer, ForeignKey('salles.id'), nullable=False)
    creneau_id = Column(Integer, ForeignKey('creneaux.id'), nullable=False)
    
    # Reservation details
    motif = Column(String(500), nullable=True)
    statut = Column(String(50), default='en_attente')  # en_attente, acceptee, rejetee
    
    # Relationships
    utilisateur = relationship("UtilisateurModel", back_populates="reservations")
    salle = relationship("SalleModel", back_populates="reservations")
    creneau = relationship("CreneauModel")
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
