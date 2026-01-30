"""Widgets personnalisés pour l'interface d'emploi du temps."""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QColor, QPalette


class SeanceCard(QFrame):
    """Widget carte pour afficher une séance de manière attractive."""
    
    def __init__(self, seance, parent=None):
        super().__init__(parent)
        self.seance = seance
        self.init_ui()
        
    def init_ui(self):
        """Initialise l'interface de la carte."""
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Style du cadre
        self.setFrameShape(QFrame.Shape.Box)
        self.setFrameShadow(QFrame.Shadow.Raised)
        self.setLineWidth(1)
        
        # Matière (titre)
        matiere_label = QLabel(self.seance.matiere.nom)
        matiere_font = QFont()
        matiere_font.setPointSize(11)
        matiere_font.setBold(True)
        matiere_label.setFont(matiere_font)
        layout.addWidget(matiere_label)
        
        # Enseignant
        enseignant_label = QLabel(f"👨‍🏫 {self.seance.enseignant.nom}")
        layout.addWidget(enseignant_label)
        
        # Salle
        salle_label = QLabel(f"🏛️ {self.seance.salle.nom}")
        layout.addWidget(salle_label)
        
        # Horaire
        horaire = f"🕐 {self.seance.creneau.heure_debut.strftime('%H:%M')} - {self.seance.creneau.heure_fin.strftime('%H:%M')}"
        horaire_label = QLabel(horaire)
        layout.addWidget(horaire_label)
        
        # Appliquer le style
        self._apply_style()
        
    def _apply_style(self):
        """Applique le style à la carte."""
        # Couleur selon le type de cours
        colors = {
            "cours": "#e3f2fd",  # Bleu clair
            "td": "#fff3e0",      # Orange clair
            "tp": "#e8f5e9"       # Vert clair
        }
        bg_color = colors.get(self.seance.matiere.type_cours, "#f5f5f5")
        
        self.setStyleSheet(f"""
            SeanceCard {{
                background-color: {bg_color};
                border: 1px solid #ddd;
                border-radius: 4px;
                padding: 8px;
                margin: 4px;
            }}
            SeanceCard:hover {{
                border: 2px solid #2196F3;
            }}
            QLabel {{
                color: #333;
                padding: 2px;
            }}
        """)


class StatCard(QFrame):
    """Widget carte pour afficher une statistique."""
    
    def __init__(self, title, value, icon="📊", parent=None):
        super().__init__(parent)
        self.title = title
        self.value = value
        self.icon = icon
        self.init_ui()
        
    def init_ui(self):
        """Initialise l'interface de la carte."""
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Style du cadre
        self.setFrameShape(QFrame.Shape.Box)
        self.setFrameShadow(QFrame.Shadow.Raised)
        
        # Icône et valeur
        value_layout = QVBoxLayout()
        
        icon_label = QLabel(self.icon)
        icon_font = QFont()
        icon_font.setPointSize(24)
        icon_label.setFont(icon_font)
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        value_layout.addWidget(icon_label)
        
        value_label = QLabel(str(self.value))
        value_font = QFont()
        value_font.setPointSize(20)
        value_font.setBold(True)
        value_label.setFont(value_font)
        value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        value_layout.addWidget(value_label)
        
        layout.addLayout(value_layout)
        
        # Titre
        title_label = QLabel(self.title)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("color: #666; font-size: 12px;")
        layout.addWidget(title_label)
        
        # Style
        self.setStyleSheet("""
            StatCard {
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 8px;
                padding: 16px;
                min-width: 150px;
            }
            StatCard:hover {
                box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            }
        """)
