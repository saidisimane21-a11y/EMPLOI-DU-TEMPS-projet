class Contrainte:
    """
    Classe de base pour représenter une contrainte sur le planning.
    Peut être étendue pour :
    - blocage de créneau pour un enseignant ou une salle
    - restriction sur certaines matières
    - règles de priorité
    """
    def est_respectee(self, seance):
        """
        Vérifie si la contrainte est respectée pour une séance donnée.
        Retourne True si ok, False sinon.
        """
        return True  # Par défaut, aucune contrainte
