from PyQt6.QtWidgets import QMessageBox


def afficher_message(parent, titre, texte):
    msg = QMessageBox(parent)
    msg.setWindowTitle(titre)
    msg.setText(texte)
    msg.exec()
