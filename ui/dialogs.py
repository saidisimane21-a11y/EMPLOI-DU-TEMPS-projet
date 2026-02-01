# -*- coding: utf-8 -*-
from PySide6.QtWidgets import (
    QDialog, QFormLayout, QLineEdit, QPushButton, 
    QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QMessageBox,
    QScrollArea, QFrame, QWidget
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from datetime import datetime
from core.salle import Salle
from core.matiere import Matiere
from core.groupe_etudiant import GroupeEtudiant
from core.creneau import Creneau
from core.enseignant import Enseignant
from core.seance import Seance
from core.reservation import Reservation
from database.models import SalleModel, MatiereModel, GroupeEtudiantModel, EnseignantModel, CreneauModel


class DialogAjouterSeance(QDialog):
    """Dialogue pour ajouter une nouvelle séance à l'emploi du temps."""
    
    def __init__(self, parent, emploi_du_temps):
        super().__init__(parent)
        self.edt = emploi_du_temps
        self.setWindowTitle("➕ Ajouter une séance")
        self.setMinimumWidth(500)
        self.setFixedHeight(600)  # Fixed height with scroll
        self.init_ui()
        self._apply_style()
        
    def init_ui(self):
        """Initialise l'interface du dialogue."""
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        
        # Titre
        title_label = QLabel("📝 Nouvelle Séance")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)

        # Scroll Area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll_content = QWidget()
        form_layout = QFormLayout(scroll_content)
        scroll.setWidget(scroll_content)
        main_layout.addWidget(scroll)
        
        # --- Matière ---
        self.input_matiere = QLineEdit()
        self.input_matiere.setPlaceholderText("Ex: Algorithmique")
        form_layout.addRow("📚 Matière:", self.input_matiere)
        
        # Code et Type sur la même ligne
        h_layout_matiere = QHBoxLayout()
        self.input_code = QLineEdit()
        self.input_code.setPlaceholderText("INFO101")
        self.combo_type_cours = QComboBox()
        self.combo_type_cours.addItems(["cours", "td", "tp"])
        h_layout_matiere.addWidget(self.input_code)
        h_layout_matiere.addWidget(QLabel("📖 Type:"))
        h_layout_matiere.addWidget(self.combo_type_cours)
        form_layout.addRow("🔢 Code:", h_layout_matiere)
        
        # Enseignant
        self.input_enseignant = QLineEdit()
        self.input_enseignant.setPlaceholderText("Ex: Dr. Dupont")
        form_layout.addRow("👨‍🏫 Enseignant:", self.input_enseignant)
        
        # --- Groupe ---
        h_layout_groupe = QHBoxLayout()
        self.input_groupe = QLineEdit()
        self.input_groupe.setPlaceholderText("G1 Info")
        self.input_filiere = QLineEdit()
        self.input_filiere.setPlaceholderText("Informatique")
        h_layout_groupe.addWidget(self.input_groupe)
        h_layout_groupe.addWidget(QLabel("🎓 Filière:"))
        h_layout_groupe.addWidget(self.input_filiere)
        form_layout.addRow("👥 Groupe:", h_layout_groupe)
        
        # Effectif
        self.input_effectif = QLineEdit()
        self.input_effectif.setPlaceholderText("Ex: 30")
        form_layout.addRow("📊 Effectif:", self.input_effectif)
        
        # --- Salle ---
        self.input_salle = QLineEdit()
        self.input_salle.setPlaceholderText("Ex: Amphi 101")
        form_layout.addRow("🏛️ Salle:", self.input_salle)
        
        # Capacité et Type salle
        h_layout_salle = QHBoxLayout()
        self.input_capacite = QLineEdit()
        self.input_capacite.setPlaceholderText("100")
        self.combo_type_salle = QComboBox()
        self.combo_type_salle.addItems(["amphi", "td", "tp", "labo"])
        h_layout_salle.addWidget(self.input_capacite)
        h_layout_salle.addWidget(QLabel("🏢 Type:"))
        h_layout_salle.addWidget(self.combo_type_salle)
        form_layout.addRow("🪑 Capacité:", h_layout_salle)
        
        # --- Temps ---
        # Jour
        self.combo_jour = QComboBox()
        self.combo_jour.addItems(["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi"])
        form_layout.addRow("📅 Jour:", self.combo_jour)
        
        # Heures sur la même ligne
        h_layout_temps = QHBoxLayout()
        self.input_debut = QLineEdit()
        self.input_debut.setPlaceholderText("08:00")
        self.input_fin = QLineEdit()
        self.input_fin.setPlaceholderText("10:00")
        h_layout_temps.addWidget(self.input_debut)
        h_layout_temps.addWidget(QLabel("à"))
        h_layout_temps.addWidget(self.input_fin)
        form_layout.addRow("🕐 Horaires:", h_layout_temps)
        
        # Boutons (en dehors de la scroll area)
        btn_layout = QHBoxLayout()
        main_layout.addLayout(btn_layout)
        
        btn_annuler = QPushButton("❌ Annuler")
        btn_annuler.clicked.connect(self.reject)
        btn_layout.addWidget(btn_annuler)
        
        btn_ajouter = QPushButton("✅ Ajouter")
        btn_ajouter.clicked.connect(self.ajouter_seance)
        btn_layout.addWidget(btn_ajouter)
        
    def ajouter_seance(self):
        """Ajoute la séance à l'emploi du temps après validation."""
        try:
            # Validation des champs obligatoires
            if not all([
                self.input_matiere.text().strip(),
                self.input_code.text().strip(),
                self.input_enseignant.text().strip(),
                self.input_groupe.text().strip(),
                self.input_filiere.text().strip(),
                self.input_salle.text().strip(),
                self.input_debut.text().strip(),
                self.input_fin.text().strip()
            ]):
                QMessageBox.warning(
                    self, 
                    "⚠️ Champs manquants",
                    "Veuillez remplir tous les champs obligatoires."
                )
                return
            
            # Validation des heures
            try:
                h_debut = datetime.strptime(
                    self.input_debut.text().strip()[:5], "%H:%M"
                ).time()
                h_fin = datetime.strptime(
                    self.input_fin.text().strip()[:5], "%H:%M"
                ).time()
            except ValueError:
                QMessageBox.warning(
                    self,
                    "⚠️ Format invalide",
                    "Le format des heures doit être HH:MM (ex: 08:00)"
                )
                return
            
            # Validation de l'effectif et capacité
            try:
                effectif = int(self.input_effectif.text().strip()) if self.input_effectif.text().strip() else 30
                capacite = int(self.input_capacite.text().strip()) if self.input_capacite.text().strip() else 100
            except ValueError:
                QMessageBox.warning(
                    self,
                    "⚠️ Valeur invalide",
                    "L'effectif et la capacité doivent être des nombres entiers."
                )
                return
            
            # Créer les objets
            creneau = Creneau(
                self.combo_jour.currentText(),
                h_debut,
                h_fin
            )
            
            salle = Salle(
                1,  # ID provisoire (sera remplacé par la DB)
                self.input_salle.text().strip(),
                capacite,
                self.combo_type_salle.currentText(),
                []  # Équipements (pour simplifier)
            )
            
            groupe = GroupeEtudiant(
                1,  # ID provisoire
                self.input_groupe.text().strip(),
                self.input_filiere.text().strip(),
                effectif
            )
            
            matiere = Matiere(
                self.input_code.text().strip(),
                self.input_matiere.text().strip(),
                self.combo_type_cours.currentText(),
                2,  # Heures par semaine par défaut
                []  # Équipements requis (pour simplifier)
            )
            
            enseignant = Enseignant(
                1,  # ID provisoire
                self.input_enseignant.text().strip(),
                [matiere],
                [creneau]
            )
            
            seance = Seance(matiere, enseignant, groupe, salle, creneau)
            
            # Ajouter la séance au domaine
            self.edt.ajouter_seance(seance)
            
            # Message de succès
            QMessageBox.information(
                self,
                "✅ Succès",
                "La séance a été ajoutée avec succès!"
            )
            
            # --- Persistence ---
            from database.base import get_session
            from database.repository import (
                SeanceRepository, SalleRepository, MatiereRepository, 
                GroupeEtudiantRepository, EnseignantRepository, CreneauRepository
            )
            session = next(get_session())
            try:
                # Check if entities exist or create them
                db_salle = session.query(SalleModel).filter_by(nom=salle.nom).first()
                if not db_salle: db_salle = SalleRepository.create(session, salle)
                
                db_matiere = session.query(MatiereModel).filter_by(code=matiere.code).first()
                if not db_matiere: db_matiere = MatiereRepository.create(session, matiere)
                
                db_groupe = session.query(GroupeEtudiantModel).filter_by(nom=groupe.nom).first()
                if not db_groupe: db_groupe = GroupeEtudiantRepository.create(session, groupe)
                
                db_enseig = session.query(EnseignantModel).filter_by(nom=enseignant.nom).first()
                if not db_enseig: db_enseig = EnseignantRepository.create(session, enseignant)
                
                db_creneau = CreneauRepository.get_or_create(session, creneau)
                
                # Create seance
                SeanceRepository.create(session, seance, db_matiere.id, db_enseig.id, db_groupe.id, db_salle.id, db_creneau.id)
                session.commit()
            except Exception as e:
                session.rollback()
                print(f"Error saving to DB: {e}")
            finally:
                session.close()

            self.accept()
            
        except ValueError as e:
            QMessageBox.critical(
                self,
                "❌ Erreur",
                f"Impossible d'ajouter la séance:\n{str(e)}"
            )
        except Exception as e:
            QMessageBox.critical(
                self,
                "❌ Erreur inattendue",
                f"Une erreur s'est produite:\n{str(e)}"
            )
    
    def _apply_style(self):
        """Applique un style au dialogue."""
        self.setStyleSheet("""
            QDialog {
                background-color: #f5f5f5;
            }
            QLabel {
                color: #333;
            }
            QLineEdit, QComboBox {
                padding: 8px;
                border: 1px solid #ccc;
                border-radius: 4px;
                background-color: white;
                min-height: 25px;
            }
            QLineEdit:focus, QComboBox:focus {
                border: 2px solid #2196F3;
            }
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 4px;
                font-weight: bold;
                min-height: 35px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QPushButton:pressed {
                background-color: #0D47A1;
            }
        """)


class DialogModifierSeance(QDialog):
    """Dialogue pour modifier une séance existante."""
    
    def __init__(self, parent, emploi_du_temps, seance):
        super().__init__(parent)
        self.edt = emploi_du_temps
        self.seance_originale = seance
        self.setWindowTitle("✏️ Modifier une séance")
        self.setMinimumWidth(500)
        self.setFixedHeight(600)
        self.init_ui()
        self._populate_fields()
        self._apply_style()
        
    def init_ui(self):
        """Initialise l'interface du dialogue."""
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        
        # Titre
        title_label = QLabel("✏️ Modifier Séance")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)

        # Scroll Area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll_content = QWidget()
        form_layout = QFormLayout(scroll_content)
        scroll.setWidget(scroll_content)
        main_layout.addWidget(scroll)
        
        # --- Matière ---
        self.input_matiere = QLineEdit()
        form_layout.addRow("📚 Matière:", self.input_matiere)
        
        # Code et Type sur la même ligne
        h_layout_matiere = QHBoxLayout()
        self.input_code = QLineEdit()
        self.combo_type_cours = QComboBox()
        self.combo_type_cours.addItems(["cours", "td", "tp"])
        h_layout_matiere.addWidget(self.input_code)
        h_layout_matiere.addWidget(QLabel("📖 Type:"))
        h_layout_matiere.addWidget(self.combo_type_cours)
        form_layout.addRow("🔢 Code:", h_layout_matiere)
        
        # Enseignant
        self.input_enseignant = QLineEdit()
        form_layout.addRow("👨‍🏫 Enseignant:", self.input_enseignant)
        
        # --- Groupe ---
        h_layout_groupe = QHBoxLayout()
        self.input_groupe = QLineEdit()
        self.input_filiere = QLineEdit()
        h_layout_groupe.addWidget(self.input_groupe)
        h_layout_groupe.addWidget(QLabel("🎓 Filière:"))
        h_layout_groupe.addWidget(self.input_filiere)
        form_layout.addRow("👥 Groupe:", h_layout_groupe)
        
        # Effectif
        self.input_effectif = QLineEdit()
        form_layout.addRow("📊 Effectif:", self.input_effectif)
        
        # --- Salle ---
        self.input_salle = QLineEdit()
        form_layout.addRow("🏛️ Salle:", self.input_salle)
        
        # Capacité et Type salle
        h_layout_salle = QHBoxLayout()
        self.input_capacite = QLineEdit()
        self.combo_type_salle = QComboBox()
        self.combo_type_salle.addItems(["amphi", "td", "tp", "labo"])
        h_layout_salle.addWidget(self.input_capacite)
        h_layout_salle.addWidget(QLabel("🏢 Type:"))
        h_layout_salle.addWidget(self.combo_type_salle)
        form_layout.addRow("🪑 Capacité:", h_layout_salle)
        
        # --- Temps ---
        # Jour
        self.combo_jour = QComboBox()
        self.combo_jour.addItems(["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi"])
        form_layout.addRow("📅 Jour:", self.combo_jour)
        
        # Heures sur la même ligne
        h_layout_temps = QHBoxLayout()
        self.input_debut = QLineEdit()
        self.input_fin = QLineEdit()
        h_layout_temps.addWidget(self.input_debut)
        h_layout_temps.addWidget(QLabel("à"))
        h_layout_temps.addWidget(self.input_fin)
        form_layout.addRow("� Horaires:", h_layout_temps)
        
        # Boutons
        btn_layout = QHBoxLayout()
        main_layout.addLayout(btn_layout)
        
        btn_annuler = QPushButton("❌ Annuler")
        btn_annuler.clicked.connect(self.reject)
        btn_layout.addWidget(btn_annuler)
        
        btn_modifier = QPushButton("✅ Modifier")
        btn_modifier.clicked.connect(self.modifier_seance)
        btn_layout.addWidget(btn_modifier)
    def _populate_fields(self):
        """Remplit les champs avec les données de la séance actuelle."""
        seance = self.seance_originale
        
        self.input_matiere.setText(seance.matiere.nom)
        self.input_code.setText(seance.matiere.code)
        self.combo_type_cours.setCurrentText(seance.matiere.type_cours)
        
        self.input_enseignant.setText(seance.enseignant.nom)
        
        self.input_groupe.setText(seance.groupe.nom)
        self.input_filiere.setText(seance.groupe.filiere)
        self.input_effectif.setText(str(seance.groupe.effectif))
        
        self.input_salle.setText(seance.salle.nom)
        self.input_capacite.setText(str(seance.salle.capacite))
        self.combo_type_salle.setCurrentText(seance.salle.type_salle)
        
        self.combo_jour.setCurrentText(seance.creneau.jour)
        self.input_debut.setText(seance.creneau.heure_debut.strftime("%H:%M"))
        self.input_fin.setText(seance.creneau.heure_fin.strftime("%H:%M"))
        
    def modifier_seance(self):
        """Modifie la séance dans l'emploi du temps."""
        try:
            # Validation des champs obligatoires
            if not all([
                self.input_matiere.text().strip(),
                self.input_code.text().strip(),
                self.input_enseignant.text().strip(),
                self.input_groupe.text().strip(),
                self.input_filiere.text().strip(),
                self.input_salle.text().strip(),
                self.input_debut.text().strip(),
                self.input_fin.text().strip()
            ]):
                QMessageBox.warning(
                    self, 
                    "⚠️ Champs manquants",
                    "Veuillez remplir tous les champs obligatoires."
                )
                return
            
            # Validation des heures
            try:
                h_debut = datetime.strptime(
                    self.input_debut.text().strip()[:5], "%H:%M"
                ).time()
                h_fin = datetime.strptime(
                    self.input_fin.text().strip()[:5], "%H:%M"
                ).time()
            except ValueError:
                QMessageBox.warning(
                    self,
                    "⚠️ Format invalide",
                    "Le format des heures doit être HH:MM (ex: 08:00)"
                )
                return
            
            # Validation de l'effectif et capacité
            try:
                effectif = int(self.input_effectif.text().strip())
                capacite = int(self.input_capacite.text().strip())
            except ValueError:
                QMessageBox.warning(
                    self,
                    "⚠️ Valeur invalide",
                    "L'effectif et la capacité doivent être des nombres entiers."
                )
                return
            
            # Créer les nouveaux objets
            creneau = Creneau(
                self.combo_jour.currentText(),
                h_debut,
                h_fin
            )
            
            salle = Salle(
                self.seance_originale.salle.id,
                self.input_salle.text().strip(),
                capacite,
                self.combo_type_salle.currentText(),
                self.seance_originale.salle.equipements
            )
            
            groupe = GroupeEtudiant(
                self.seance_originale.groupe.id,
                self.input_groupe.text().strip(),
                self.input_filiere.text().strip(),
                effectif
            )
            
            matiere = Matiere(
                self.input_code.text().strip(),
                self.input_matiere.text().strip(),
                self.combo_type_cours.currentText(),
                self.seance_originale.matiere.volume_horaire,
                self.seance_originale.matiere.equipements_requis
            )
            
            enseignant = Enseignant(
                self.seance_originale.enseignant.id,
                self.input_enseignant.text().strip(),
                [matiere],
                [creneau]
            )
            
            nouvelle_seance = Seance(matiere, enseignant, groupe, salle, creneau)

            # Supprimer l'ancienne séance du domaine
            self.edt.supprimer_seance(self.seance_originale)
            
            # Ajouter la nouvelle séance au domaine
            self.edt.ajouter_seance(nouvelle_seance)
            
            # --- Persistence ---
            from database.base import get_session
            from database.repository import (
                SeanceRepository, SalleRepository, MatiereRepository, 
                GroupeEtudiantRepository, EnseignantRepository, CreneauRepository
            )
            session = next(get_session())
            try:
                # 1. Delete old one
                SeanceRepository.delete_by_details(session, self.seance_originale)
                
                # 2. Add new one (check/create parents)
                db_salle = session.query(SalleModel).filter_by(nom=salle.nom).first()
                if not db_salle: db_salle = SalleRepository.create(session, salle)
                
                db_matiere = session.query(MatiereModel).filter_by(code=matiere.code).first()
                if not db_matiere: db_matiere = MatiereRepository.create(session, matiere)
                
                db_groupe = session.query(GroupeEtudiantModel).filter_by(nom=groupe.nom).first()
                if not db_groupe: db_groupe = GroupeEtudiantRepository.create(session, groupe)
                
                db_enseig = session.query(EnseignantModel).filter_by(nom=enseignant.nom).first()
                if not db_enseig: db_enseig = EnseignantRepository.create(session, enseignant)
                
                db_creneau = CreneauRepository.get_or_create(session, creneau)
                
                SeanceRepository.create(session, nouvelle_seance, db_matiere.id, db_enseig.id, db_groupe.id, db_salle.id, db_creneau.id)
                session.commit()
            except Exception as e:
                session.rollback()
                print(f"Error updating DB: {e}")
            finally:
                session.close()
            
            # Message de succès
            QMessageBox.information(
                self,
                "✅ Succès",
                "La séance a été modifiée avec succès!"
            )
            
            self.accept()
            
        except ValueError as e:
            # Remettre l'ancienne séance si échec
            try:
                self.edt.ajouter_seance(self.seance_originale)
            except:
                pass
            QMessageBox.critical(
                self,
                "❌ Erreur",
                f"Impossible de modifier la séance:\n{str(e)}"
            )
        except Exception as e:
            # Remettre l'ancienne séance si échec
            try:
                self.edt.ajouter_seance(self.seance_originale)
            except:
                pass
            QMessageBox.critical(
                self,
                "❌ Erreur inattendue",
                f"Une erreur s'est produite:\n{str(e)}"
            )
    
    def _apply_style(self):
        """Applique un style au dialogue."""
        self.setStyleSheet("""
            QDialog {
                background-color: #f5f5f5;
            }
            QLabel {
                color: #333;
            }
            QLineEdit, QComboBox {
                padding: 8px;
                border: 1px solid #ccc;
                border-radius: 4px;
                background-color: white;
                min-height: 25px;
            }
            QLineEdit:focus, QComboBox:focus {
                border: 2px solid #2196F3;
            }
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 4px;
                font-weight: bold;
                min-height: 35px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QPushButton:pressed {
                background-color: #0D47A1;
            }
        """)


class DialogReservation(QDialog):
    """Dialogue pour effectuer une demande de réservation de salle."""
    
    def __init__(self, parent, utilisateur):
        super().__init__(parent)
        self.utilisateur = utilisateur
        self.setWindowTitle("📅 Réserver une salle")
        self.setMinimumWidth(450)
        self.setFixedHeight(500)
        self.init_ui()
        self._apply_style()
        
    def init_ui(self):
        """Initialise l'interface du dialogue."""
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        
        # Titre
        title_label = QLabel("🏛️ Demande de Réservation")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)

        # Scroll Area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll_content = QWidget()
        form_layout = QFormLayout(scroll_content)
        scroll.setWidget(scroll_content)
        main_layout.addWidget(scroll)
        
        # Salle
        self.combo_salle = QComboBox()
        self._load_salles()
        form_layout.addRow("🏛️ Salle:", self.combo_salle)
        
        # Jour
        self.combo_jour = QComboBox()
        self.combo_jour.addItems([
            "Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi"
        ])
        form_layout.addRow("📅 Jour:", self.combo_jour)
        
        # Heures sur la même ligne
        h_layout_temps = QHBoxLayout()
        self.input_debut = QLineEdit()
        self.input_debut.setPlaceholderText("08:00")
        self.input_fin = QLineEdit()
        self.input_fin.setPlaceholderText("10:00")
        h_layout_temps.addWidget(self.input_debut)
        h_layout_temps.addWidget(QLabel("à"))
        h_layout_temps.addWidget(self.input_fin)
        form_layout.addRow("� Horaires:", h_layout_temps)
        
        # Motif
        self.input_motif = QLineEdit()
        self.input_motif.setPlaceholderText("Ex: Réunion de projet...")
        form_layout.addRow("📝 Motif:", self.input_motif)
        
        # Boutons
        btn_layout = QHBoxLayout()
        main_layout.addLayout(btn_layout)
        
        btn_annuler = QPushButton("❌ Annuler")
        btn_annuler.clicked.connect(self.reject)
        btn_layout.addWidget(btn_annuler)
        
        btn_reserver = QPushButton("✅ Réserver")
        btn_reserver.clicked.connect(self.effectuer_reservation)
        btn_layout.addWidget(btn_reserver)
        
    def _load_salles(self):
        """Charge la liste des salles depuis la base de données."""
        from database.base import get_session
        from database.repository import SalleRepository
        session = next(get_session())
        try:
            salles = SalleRepository.get_all(session)
            for s in salles:
                self.combo_salle.addItem(s.nom, s)
        finally:
            session.close()

    def effectuer_reservation(self):
        """Enregistre la demande de réservation."""
        try:
            if not all([self.input_debut.text(), self.input_fin.text()]):
                QMessageBox.warning(self, "⚠️ Champs manquants", "Veuillez remplir les heures.")
                return

            try:
                h_debut = datetime.strptime(self.input_debut.text().strip()[:5], "%H:%M").time()
                h_fin = datetime.strptime(self.input_fin.text().strip()[:5], "%H:%M").time()
            except ValueError:
                QMessageBox.warning(self, "⚠️ Format invalide", "Format HH:MM requis.")
                return

            creneau = Creneau(self.combo_jour.currentText(), h_debut, h_fin)
            salle = self.combo_salle.currentData()
            motif = self.input_motif.text()

            reservation = Reservation(self.utilisateur, salle, creneau, motif)

            # Persistence
            from database.base import get_session
            from database.repository import ReservationRepository
            session = next(get_session())
            try:
                ReservationRepository.create(session, reservation, self.utilisateur.id)
                QMessageBox.information(self, "✅ Succès", "Votre demande de réservation a été envoyée.")
                self.accept()
            except Exception as e:
                session.rollback()
                QMessageBox.critical(self, "❌ Erreur", f"Erreur lors de l'enregistrement: {e}")
            finally:
                session.close()

        except Exception as e:
            QMessageBox.critical(self, "❌ Erreur", str(e))

    def _apply_style(self):
        """Applique le style uniformisé."""
        self.setStyleSheet("""
            QDialog { background-color: #f5f5f5; }
            QLabel { color: #333; }
            QLineEdit, QComboBox {
                padding: 8px; border: 1px solid #ccc;
                border-radius: 4px; background-color: white;
            }
            QPushButton {
                background-color: #4CAF50; color: white;
                border: none; padding: 10px; border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #45a049; }
        """)
