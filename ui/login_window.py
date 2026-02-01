# -*- coding: utf-8 -*-
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
    QLineEdit, QPushButton, QMessageBox, QWidget
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QIcon
from database.base import get_session
from database.repository import UtilisateurRepository

class LoginWindow(QDialog):
    """Fenêtre de connexion simple et élégante."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.user = None
        self.init_ui()
        self._apply_style()
        
    def init_ui(self):
        self.setWindowTitle("Connexion - Emploi du Temps")
        self.setFixedSize(400, 300)
        
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Titre
        title_label = QLabel("🚀 Bienvenue")
        title_label.setAlignment(Qt.AlignCenter)
        title_font = QFont("Segoe UI", 24, QFont.Bold)
        title_label.setFont(title_font)
        layout.addWidget(title_label)
        
        subtitle = QLabel("Connectez-vous pour accéder à votre espace")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color: #666; margin-bottom: 20px;")
        layout.addWidget(subtitle)
        
        # Formulaire
        form_layout = QVBoxLayout()
        form_layout.setSpacing(15)
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Nom d'utilisateur")
        self.username_input.setMinimumHeight(40)
        form_layout.addWidget(self.username_input)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Mot de passe")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setMinimumHeight(40)
        form_layout.addWidget(self.password_input)
        
        layout.addLayout(form_layout)
        
        # Bouton
        self.login_button = QPushButton("Se connecter")
        self.login_button.setMinimumHeight(45)
        self.login_button.setCursor(Qt.PointingHandCursor)
        self.login_button.clicked.connect(self.handle_login)
        layout.addWidget(self.login_button)
        
        layout.addStretch()
        
    def _apply_style(self):
        self.setStyleSheet("""
            QDialog {
                background-color: white;
            }
            QLineEdit {
                border: 2px solid #eee;
                border-radius: 8px;
                padding-left: 10px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 2px solid #2196F3;
            }
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
                margin-top: 10px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)

    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        
        if not username or not password:
            QMessageBox.warning(self, "Erreur", "Veuillez remplir tous les champs.")
            return
            
        session = next(get_session())
        try:
            db_user = UtilisateurRepository.authenticate(session, username, password)
            if db_user:
                self.user = db_user
                self.accept()
            else:
                QMessageBox.critical(self, "Erreur", "Nom d'utilisateur ou mot de passe incorrect.")
        finally:
            session.close()
