from datetime import time


class Creneau:
    """
    Représente un créneau horaire immuable.
    Un créneau est défini par un jour, une heure de début et une heure de fin.
    """

    JOURS_VALIDES = {
        "lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi"
    }

    def __init__(self, jour: str, heure_debut: time, heure_fin: time):
        self._valider_jour(jour)
        self._valider_heures(heure_debut, heure_fin)

        self._jour = jour.lower()
        self._heure_debut = heure_debut
        self._heure_fin = heure_fin

    # --------------------
    # Propriétés (lecture seule)
    # --------------------
    @property
    def jour(self):
        return self._jour

    @property
    def heure_debut(self):
        return self._heure_debut

    @property
    def heure_fin(self):
        return self._heure_fin

    # --------------------
    # Logique métier
    # --------------------
    def chevauche(self, autre: "Creneau") -> bool:
        """
        Retourne True si deux créneaux se chevauchent.
        """
        if self.jour != autre.jour:
            return False

        return not (
            self.heure_fin <= autre.heure_debut
            or autre.heure_fin <= self.heure_debut
        )

    # --------------------
    # Méthodes utilitaires
    # --------------------
    def _valider_jour(self, jour: str):
        if not isinstance(jour, str):
            raise TypeError("Le jour doit être une chaîne de caractères.")

        if jour.lower() not in self.JOURS_VALIDES:
            raise ValueError(
                f"Jour invalide : {jour}. Jours autorisés : {self.JOURS_VALIDES}"
            )

    def _valider_heures(self, debut: time, fin: time):
        if not isinstance(debut, time) or not isinstance(fin, time):
            raise TypeError("Les heures doivent être de type datetime.time.")

        if debut >= fin:
            raise ValueError(
                "L'heure de début doit être strictement inférieure à l'heure de fin."
            )

    # --------------------
    # Représentations
    # --------------------
    def __str__(self):
        return f"{self.jour.capitalize()} {self.heure_debut} - {self.heure_fin}"

    def __eq__(self, autre):
        if not isinstance(autre, Creneau):
            return False
        return (
            self.jour == autre.jour
            and self.heure_debut == autre.heure_debut
            and self.heure_fin == autre.heure_fin
        )

    def __hash__(self):
        return hash((self.jour, self.heure_debut, self.heure_fin))
