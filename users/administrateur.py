from users.utilisateur import Utilisateur

class Administrateur(Utilisateur):
    """
    Administrateur : peut générer et valider les emplois du temps.
    """

    def generer_planning(self, emploi_du_temps, seances_a_ajouter):
        """
        Ajoute plusieurs séances à l'emploi du temps.
        """
        for seance in seances_a_ajouter:
            emploi_du_temps.ajouter_seance(seance)

    def valider_reservation(self, reservation):
        """
        Valide ou rejette une demande de réservation.
        """
        reservation.validee = True

    def consulter_emploi_du_temps(self, emploi_du_temps):
        return emploi_du_temps.seances
