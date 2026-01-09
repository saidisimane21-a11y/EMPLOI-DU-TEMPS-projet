class ConflitException(Exception):
    """
    Exception levée lorsqu'une séance entre en conflit
    avec l'emploi du temps existant ou une autre règle métier.
    """
    pass

class DisponibiliteException(Exception):
    """
    Exception levée lorsqu'un enseignant ou une salle
    n'est pas disponible sur le créneau demandé.
    """
    pass

class CompatibiliteSalleException(Exception):
    """
    Exception levée lorsqu'une salle n'est pas compatible
    avec le groupe ou la matière (effectif / équipements).
    """
    pass
