from faker import Faker

from desk_reservation.seats.application.seat_getter import SeatGetter


def test__seat_getter__was_called_correctly(mocker, seat_factory):
    seat_id=Faker().uuid4()
    seat_service = mocker.Mock()
    seat_getter = SeatGetter(seat_service=seat_service)
    
    seat_getter.execute(seat_id=seat_id)
    
    seat_getter.seat_service.get_seat_by_id.assert_called_with(seat_id)
   