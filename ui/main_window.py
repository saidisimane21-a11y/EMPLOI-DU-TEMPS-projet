from PySide6.QtWidgets import (
    QMainWindow, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QPushButton, QComboBox, QWidget, QLabel,
    QHBoxLayout, QMessageBox, QHeaderView, QTabWidget, QFileDialog
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QColor
from users.administrateur import Administrateur
import csv
from datetime import datetime


class MainWindow(QMainWindow):
    """Fenêtre principale de l'application d'emploi du temps."""
    
    def __init__(self, emploi_du_temps, utilisateur=None):
        super().__init__()
        self.edt = emploi_du_temps
        self.utilisateur = utilisateur
        self.init_ui()
        
    def init_ui(self):
        """Initialise l'interface utilisateur."""
        self.setWindowTitle("📚 Gestion d'Emploi du Temps - Dashboard")
        self.setGeometry(100, 100, 1200, 700)
        
        # Widget central avec onglets
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # En-tête avec nom d'utilisateur
        self._create_header(main_layout)
        
        # Onglets
        tabs = QTabWidget()
        main_layout.addWidget(tabs)
        
        # Onglet 1: Vue Tableau
        tab_table = QWidget()
        tabs.addTab(tab_table, "📋 Vue Tableau")
        self._create_table_view(tab_table)
        
        # Onglet 2: Vue Calendrier (simple)
        tab_calendar = QWidget()
        tabs.addTab(tab_calendar, "📅 Vue Calendrier")
        self._create_calendar_view(tab_calendar)
        
        # Appliquer le style
        self._apply_style()
        
    def _create_header(self, parent_layout):
        """Crée l'en-tête de l'application."""
        header_layout = QHBoxLayout()
        parent_layout.addLayout(header_layout)
        
        title_label = QLabel("📚 Emploi du Temps")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title_label.setFont(title_font)
        header_layout.addWidget(title_label)
        
        header_layout.addStretch()
        
        if self.utilisateur:
            user_label = QLabel(f"👤 {self.utilisateur.nom}")
            user_label.setStyleSheet("color: #666; font-size: 14px;")
            header_layout.addWidget(user_label)
            
    def _create_table_view(self, parent):
        """Crée la vue tableau des séances."""
        layout = QVBoxLayout()
        parent.setLayout(layout)
        
        # --- Filtres ---
        filter_layout = QHBoxLayout()
        layout.addLayout(filter_layout)
        
        filter_label = QLabel("🔍 Filtres:")
        filter_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        filter_layout.addWidget(filter_label)
        
        # Filtre enseignant
        filter_layout.addWidget(QLabel("Enseignant:"))
        self.combo_enseignant = QComboBox()
        self.combo_enseignant.setMinimumWidth(150)
        self.combo_enseignant.addItem("Tous")
        enseignants = sorted({s.enseignant.nom for s in self.edt.seances})
        for nom in enseignants:
            self.combo_enseignant.addItem(nom)
        filter_layout.addWidget(self.combo_enseignant)
        
        # Filtre groupe
        filter_layout.addWidget(QLabel("Groupe:"))
        self.combo_groupe = QComboBox()
        self.combo_groupe.setMinimumWidth(150)
        self.combo_groupe.addItem("Tous")
        groupes = sorted({s.groupe.nom for s in self.edt.seances})
        for nom in groupes:
            self.combo_groupe.addItem(nom)
        filter_layout.addWidget(self.combo_groupe)
        
        # Filtre salle
        filter_layout.addWidget(QLabel("Salle:"))
        self.combo_salle = QComboBox()
        self.combo_salle.setMinimumWidth(150)
        self.combo_salle.addItem("Toutes")
        salles = sorted({s.salle.nom for s in self.edt.seances})
        for nom in salles:
            self.combo_salle.addItem(nom)
        filter_layout.addWidget(self.combo_salle)
        
        filter_layout.addStretch()
        
        # Connecter les filtres
        self.combo_enseignant.currentTextChanged.connect(self.afficher_emploi_du_temps)
        self.combo_groupe.currentTextChanged.connect(self.afficher_emploi_du_temps)
        self.combo_salle.currentTextChanged.connect(self.afficher_emploi_du_temps)
        
        # --- Table ---
        self.table = QTableWidget()
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        layout.addWidget(self.table)
        
        # --- Boutons d'action ---
        btn_layout = QHBoxLayout()
        layout.addLayout(btn_layout)
        
        # Statistiques
        self.label_stats = QLabel(f"Total: {len(self.edt.seances)} séances")
        self.label_stats.setStyleSheet("font-weight: bold; color: #2196F3;")
        btn_layout.addWidget(self.label_stats)
        
        btn_layout.addStretch()
        
        # Boutons d'action (pour Admin)
        if isinstance(self.utilisateur, Administrateur):
            self.btn_ajouter = QPushButton("➕ Ajouter")
            self.btn_ajouter.setMinimumHeight(35)
            self.btn_ajouter.clicked.connect(self.ouvrir_dialog_ajout_seance)
            btn_layout.addWidget(self.btn_ajouter)
            
            self.btn_modifier = QPushButton("✏️ Modifier")
            self.btn_modifier.setMinimumHeight(35)
            self.btn_modifier.clicked.connect(self.modifier_seance)
            btn_layout.addWidget(self.btn_modifier)
            
            self.btn_supprimer = QPushButton("🗑️ Supprimer")
            self.btn_supprimer.setMinimumHeight(35)
            self.btn_supprimer.setStyleSheet("""
                QPushButton {
                    background-color: #f44336;
                }
                QPushButton:hover {
                    background-color: #d32f2f;
                }
            """)
            self.btn_supprimer.clicked.connect(self.supprimer_seance)
            btn_layout.addWidget(self.btn_supprimer)
        
        # Bouton Exporter (pour tous)
        self.btn_exporter = QPushButton("📥 Exporter")
        self.btn_exporter.setMinimumHeight(35)
        self.btn_exporter.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
            }
            QPushButton:hover {
                background-color: #388E3C;
            }
        """)
        self.btn_exporter.clicked.connect(self.exporter_emploi_du_temps)
        btn_layout.addWidget(self.btn_exporter)
            
        # Affichage initial
        self.afficher_emploi_du_temps()
        
    def _create_calendar_view(self, parent):
        """Crée une vue calendrier simple."""
        layout = QVBoxLayout()
        parent.setLayout(layout)
        
        info_label = QLabel("📅 Vue Calendrier hebdomadaire")
        info_label.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px;")
        layout.addWidget(info_label)
        
        # Table pour le calendrier
        self.calendar_table = QTableWidget()
        self.calendar_table.setColumnCount(6)  # Jours de la semaine
        self.calendar_table.setHorizontalHeaderLabels([
            "Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi"
        ])
        
        # Remplir le calendrier
        self._fill_calendar()
        
        layout.addWidget(self.calendar_table)
        
    def _fill_calendar(self):
        """Remplit la vue calendrier avec les séances."""
        # Regrouper par jour et créneau
        jours = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi"]
        
        # Créer une structure pour stocker les créneaux par jour
        calendar_data = {jour: {} for jour in jours}
        
        for seance in self.edt.seances:
            jour = seance.creneau.jour
            if jour in calendar_data:
                creneau_key = f"{seance.creneau.heure_debut.strftime('%H:%M')}-{seance.creneau.heure_fin.strftime('%H:%M')}"
                if creneau_key not in calendar_data[jour]:
                    calendar_data[jour][creneau_key] = []
                calendar_data[jour][creneau_key].append(seance)
        
        # Déterminer le nombre de lignes nécessaires (créneaux horaires)
        all_creneaux = set()
        for jour_data in calendar_data.values():
            all_creneaux.update(jour_data.keys())
        
        creneaux_list = sorted(list(all_creneaux))
        self.calendar_table.setRowCount(len(creneaux_list) if creneaux_list else 1)
        self.calendar_table.setVerticalHeaderLabels(creneaux_list if creneaux_list else [""])
        
        # Remplir la table
        for col, jour in enumerate(jours):
            for row, creneau in enumerate(creneaux_list):
                if creneau in calendar_data[jour]:
                    seances_text = "\n".join([
                        f"{s.matiere.nom}\n{s.enseignant.nom}\n{s.salle.nom}"
                        for s in calendar_data[jour][creneau]
                    ])
                    item = QTableWidgetItem(seances_text)
                    item.setBackground(QColor("#e3f2fd"))
                    self.calendar_table.setItem(row, col, item)
                else:
                    self.calendar_table.setItem(row, col, QTableWidgetItem(""))
        
        # Ajuster les tailles
        self.calendar_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.calendar_table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        
    def afficher_emploi_du_temps(self):
        """Affiche l'emploi du temps avec les filtres appliqués."""
        seances = self._get_filtered_seances()
        
        # Mise à jour des statistiques
        self.label_stats.setText(f"Affichage: {len(seances)} / {len(self.edt.seances)} séances")
        
        # Remplir la table
        self.table.setRowCount(len(seances))
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "Matière", "Enseignant", "Groupe", "Salle", "Jour", "Horaire"
        ])
        
        for i, s in enumerate(seances):
            # Matière
            item_matiere = QTableWidgetItem(s.matiere.nom)
            item_matiere.setFont(QFont("Arial", 10, QFont.Weight.Bold))
            self.table.setItem(i, 0, item_matiere)
            
            # Enseignant
            self.table.setItem(i, 1, QTableWidgetItem(s.enseignant.nom))
            
            # Groupe
            self.table.setItem(i, 2, QTableWidgetItem(s.groupe.nom))
            
            # Salle
            self.table.setItem(i, 3, QTableWidgetItem(s.salle.nom))
            
            # Jour
            self.table.setItem(i, 4, QTableWidgetItem(s.creneau.jour))
            
            # Horaire
            horaire = f"{s.creneau.heure_debut.strftime('%H:%M')} - {s.creneau.heure_fin.strftime('%H:%M')}"
            self.table.setItem(i, 5, QTableWidgetItem(horaire))
        
        # Ajuster les colonnes
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        
    def ouvrir_dialog_ajout_seance(self):
        """Ouvre le dialogue pour ajouter une séance."""
        from ui.dialogs import DialogAjouterSeance
        
        dialog = DialogAjouterSeance(self, self.edt)
        if dialog.exec():
            # Rafraîchir l'affichage
            self.afficher_emploi_du_temps()
            self._fill_calendar()
            
            # Mettre à jour les filtres si nécessaire
            self._update_filters()
    
    def modifier_seance(self):
        """Modifie la séance sélectionnée."""
        selected_row = self.table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(
                self,
                "⚠️ Aucune sélection",
                "Veuillez sélectionner une séance à modifier."
            )
            return
        
        # Obtenir la séance filtrée correspondante
        seances_filtrees = self._get_filtered_seances()
        if selected_row >= len(seances_filtrees):
            return
            
        seance = seances_filtrees[selected_row]
        
        from ui.dialogs import DialogModifierSeance
        dialog = DialogModifierSeance(self, self.edt, seance)
        if dialog.exec():
            self.afficher_emploi_du_temps()
            self._fill_calendar()
            self._update_filters()
    
    def supprimer_seance(self):
        """Supprime la séance sélectionnée."""
        selected_row = self.table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(
                self,
                "⚠️ Aucune sélection",
                "Veuillez sélectionner une séance à supprimer."
            )
            return
        
        # Obtenir la séance filtrée correspondante
        seances_filtrees = self._get_filtered_seances()
        if selected_row >= len(seances_filtrees):
            return
            
        seance = seances_filtrees[selected_row]
        
        # Confirmation
        reply = QMessageBox.question(
            self,
            "❓ Confirmation",
            f"Voulez-vous vraiment supprimer cette séance ?\n\n"
            f"Matière: {seance.matiere.nom}\n"
            f"Enseignant: {seance.enseignant.nom}\n"
            f"Groupe: {seance.groupe.nom}\n"
            f"{seance.creneau.jour} {seance.creneau.heure_debut.strftime('%H:%M')}-{seance.creneau.heure_fin.strftime('%H:%M')}",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.edt.supprimer_seance(seance)
            QMessageBox.information(
                self,
                "✅ Succès",
                "La séance a été supprimée avec succès."
            )
            self.afficher_emploi_du_temps()
            self._fill_calendar()
            self._update_filters()
    
    def exporter_emploi_du_temps(self):
        """Exporte l'emploi du temps au format CSV."""
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Exporter l'emploi du temps",
            f"emploi_du_temps_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            "CSV Files (*.csv);;All Files (*)"
        )
        
        if not file_path:
            return
        
        try:
            with open(file_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
                writer = csv.writer(csvfile)
                
                # En-têtes
                writer.writerow(['Matière', 'Code', 'Type', 'Enseignant', 'Groupe', 
                                'Filière', 'Salle', 'Type Salle', 'Jour', 'Heure Début', 'Heure Fin'])
                
                # Données
                for seance in self.edt.seances:
                    writer.writerow([
                        seance.matiere.nom,
                        seance.matiere.code,
                        seance.matiere.type_cours,
                        seance.enseignant.nom,
                        seance.groupe.nom,
                        seance.groupe.filiere,
                        seance.salle.nom,
                        seance.salle.type_salle,
                        seance.creneau.jour,
                        seance.creneau.heure_debut.strftime('%H:%M'),
                        seance.creneau.heure_fin.strftime('%H:%M')
                    ])
            
            QMessageBox.information(
                self,
                "✅ Succès",
                f"L'emploi du temps a été exporté avec succès vers:\n{file_path}"
            )
        except Exception as e:
            QMessageBox.critical(
                self,
                "❌ Erreur",
                f"Erreur lors de l'exportation:\n{str(e)}"
            )
    
    def _get_filtered_seances(self):
        """Retourne les séances filtrées selon les critères actuels."""
        seances = self.edt.seances
        
        enseignant_sel = self.combo_enseignant.currentText()
        if enseignant_sel != "Tous":
            seances = [s for s in seances if s.enseignant.nom == enseignant_sel]
            
        groupe_sel = self.combo_groupe.currentText()
        if groupe_sel != "Tous":
            seances = [s for s in seances if s.groupe.nom == groupe_sel]
            
        salle_sel = self.combo_salle.currentText()
        if salle_sel != "Toutes":
            seances = [s for s in seances if s.salle.nom == salle_sel]
        
        return seances
    
    def _update_filters(self):
        """Met à jour les listes de filtres."""
        # Sauvegarder les sélections actuelles
        current_enseignant = self.combo_enseignant.currentText()
        current_groupe = self.combo_groupe.currentText()
        current_salle = self.combo_salle.currentText()
        
        # Mettre à jour enseignants
        self.combo_enseignant.clear()
        self.combo_enseignant.addItem("Tous")
        enseignants = sorted({s.enseignant.nom for s in self.edt.seances})
        for nom in enseignants:
            self.combo_enseignant.addItem(nom)
        idx = self.combo_enseignant.findText(current_enseignant)
        if idx >= 0:
            self.combo_enseignant.setCurrentIndex(idx)
            
        # Mettre à jour groupes
        self.combo_groupe.clear()
        self.combo_groupe.addItem("Tous")
        groupes = sorted({s.groupe.nom for s in self.edt.seances})
        for nom in groupes:
            self.combo_groupe.addItem(nom)
        idx = self.combo_groupe.findText(current_groupe)
        if idx >= 0:
            self.combo_groupe.setCurrentIndex(idx)
            
        # Mettre à jour salles
        self.combo_salle.clear()
        self.combo_salle.addItem("Toutes")
        salles = sorted({s.salle.nom for s in self.edt.seances})
        for nom in salles:
            self.combo_salle.addItem(nom)
        idx = self.combo_salle.findText(current_salle)
        if idx >= 0:
            self.combo_salle.setCurrentIndex(idx)
            
    def _apply_style(self):
        """Applique un style moderne à l'application."""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QWidget {
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 12px;
            }
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QPushButton:pressed {
                background-color: #0D47A1;
            }
            QComboBox {
                padding: 5px;
                border: 1px solid #ccc;
                border-radius: 4px;
                background-color: white;
            }
            QTableWidget {
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 4px;
                gridline-color: #e0e0e0;
            }
            QTableWidget::item {
                padding: 8px;
            }
            QTableWidget::item:selected {
                background-color: #2196F3;
                color: white;
            }
            QHeaderView::section {
                background-color: #1976D2;
                color: white;
                padding: 8px;
                border: none;
                font-weight: bold;
            }
            QTabWidget::pane {
                border: 1px solid #ddd;
                background-color: white;
                border-radius: 4px;
            }
            QTabBar::tab {
                background-color: #e0e0e0;
                padding: 10px 20px;
                margin-right: 2px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            QTabBar::tab:selected {
                background-color: white;
                color: #2196F3;
                font-weight: bold;
            }
            QTabBar::tab:hover {
                background-color: #d0d0d0;
            }
        """)