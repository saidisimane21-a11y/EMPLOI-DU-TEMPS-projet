from PyQt6.QtWidgets import (
    QMainWindow, QApplication, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QPushButton, QLineEdit, QComboBox, QWidget, QLabel,
    QFormLayout, QHBoxLayout, QDialog
)
from PyQt6.QtCore import Qt
from datetime import datetime
from core.salle import Salle
from core.groupe import GroupeEtudiant
from core.matiere import Matiere
from core.creneau import Creneau
from core.enseignant import Enseignant
from core.seance import Seance
from users import Administrateur, EnseignantUser, Etudiant


class MainWindow(QMainWindow):
    def __init__(self, emploi_du_temps, utilisateur=None):
        super().__init__()
        self.setWindowTitle("Emploi du Temps - Mini Dashboard")
        self.setGeometry(100, 100, 900, 500)
        self.edt = emploi_du_temps
        self.utilisateur = utilisateur

        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # --- Filtres ---
        filter_layout = QHBoxLayout()
        main_layout.addLayout(filter_layout)

        filter_layout.addWidget(QLabel("Filtrer par enseignant:"))
        self.combo_enseignant = QComboBox()
        self.combo_enseignant.addItem("Tous")
        enseignants = {s.enseignant.nom for s in self.edt.seances}
        for nom in enseignants:
            self.combo_enseignant.addItem(nom)
        filter_layout.addWidget(self.combo_enseignant)

        filter_layout.addWidget(QLabel("Filtrer par groupe:"))
        self.combo_groupe = QComboBox()
        self.combo_groupe.addItem("Tous")
        groupes = {s.groupe.nom for s in self.edt.seances}
        for nom in groupes:
            self.combo_groupe.addItem(nom)
        filter_layout.addWidget(self.combo_groupe)

        # Connecter les filtres
        self.combo_enseignant.currentTextChanged.connect(
            self.afficher_emploi_du_temps)
        self.combo_groupe.currentTextChanged.connect(
            self.afficher_emploi_du_temps)

        # --- Table ---
        self.table = QTableWidget()
        main_layout.addWidget(self.table)

        # --- Bouton Ajouter séance pour Admin ---
        if isinstance(self.utilisateur, Administrateur):
            self.btn_ajouter_seance = QPushButton("Ajouter une séance")
            self.btn_ajouter_seance.clicked.connect(
                self.ouvrir_dialog_ajout_seance)
            main_layout.addWidget(self.btn_ajouter_seance)

        # Affichage initial
        self.afficher_emploi_du_temps()

    def afficher_emploi_du_temps(self):
        seances = self.edt.seances

        # Filtrer enseignant
        enseignant_sel = self.combo_enseignant.currentText()
        if enseignant_sel != "Tous":
            seances = [s for s in seances if s.enseignant.nom == enseignant_sel]

        # Filtrer groupe
        groupe_sel = self.combo_groupe.currentText()
        if groupe_sel != "Tous":
            seances = [s for s in seances if s.groupe.nom == groupe_sel]

        # Remplir la table
        self.table.setRowCount(len(seances))
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(
            ["Matière", "Enseignant", "Groupe", "Salle", "Créneau"]
        )

        for i, s in enumerate(seances):
            self.table.setItem(i, 0, QTableWidgetItem(s.matiere.nom))
            self.table.setItem(i, 1, QTableWidgetItem(s.enseignant.nom))
            self.table.setItem(i, 2, QTableWidgetItem(s.groupe.nom))
            self.table.setItem(i, 3, QTableWidgetItem(s.salle.nom))
            self.table.setItem(i, 4, QTableWidgetItem(str(s.creneau)))

        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()

    def ouvrir_dialog_ajout_seance(self):
        dialog = DialogAjouterSeance(self)
        dialog.exec()
        self.afficher_emploi_du_temps()


class DialogAjouterSeance(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Ajouter une séance")
        self.parent = parent

        layout = QFormLayout()
        self.setLayout(layout)

        # Champs pour la saisie
        self.input_matiere = QLineEdit()
        self.input_enseignant = QLineEdit()
        self.input_groupe = QLineEdit()
        self.input_salle = QLineEdit()
        self.input_jour = QLineEdit()
        self.input_debut = QLineEdit()
        self.input_fin = QLineEdit()

        layout.addRow("Matière:", self.input_matiere)
        layout.addRow("Enseignant:", self.input_enseignant)
        layout.addRow("Groupe:", self.input_groupe)
        layout.addRow("Salle:", self.input_salle)
        layout.addRow("Jour:", self.input_jour)
        layout.addRow("Heure début (HH:MM):", self.input_debut)
        layout.addRow("Heure fin (HH:MM):", self.input_fin)

        btn_ok = QPushButton("Ajouter")
        btn_ok.clicked.connect(self.ajouter_seance)
        layout.addWidget(btn_ok)

    def ajouter_seance(self):
      # On prend seulement les 5 premiers caractères pour éviter les secondes
      h_debut = datetime.strptime(
          self.input_debut.text().strip()[:5], "%H:%M").time()
      h_fin = datetime.strptime(
          self.input_fin.text().strip()[:5], "%H:%M").time()

      creneau = Creneau(self.input_jour.text().strip(), h_debut, h_fin)

      salle = Salle(0, self.input_salle.text().strip(), 30, "td", [])
      groupe = GroupeEtudiant(0, self.input_groupe.text().strip(), "filiere", 20)
      matiere = Matiere(
          "CODE", self.input_matiere.text().strip(), "cours", 2, [])
      enseignant = Enseignant(
          0, self.input_enseignant.text().strip(), [matiere], [creneau])

      seance = Seance(matiere, enseignant, groupe, salle, creneau)
      self.parent.edt.ajouter_seance(seance)
      self.accept()
