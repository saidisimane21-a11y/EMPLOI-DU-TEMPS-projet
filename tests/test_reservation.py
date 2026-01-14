from core.reservation import Reservation

def test_reservation_statut():
    r = Reservation("ens", "salle", "creneau")
    assert r.statut == Reservation.PENDING

    r.accepter()
    assert r.statut == Reservation.ACCEPTED
