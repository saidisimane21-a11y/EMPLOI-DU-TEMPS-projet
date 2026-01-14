from enum import Enum

class ConflictType(Enum):
    SALLE = "Conflit de salle"
    ENSEIGNANT = "Conflit d'enseignant"
    GROUPE = "Conflit de groupe"
    CRENEAU = "Chevauchement de créneau"
