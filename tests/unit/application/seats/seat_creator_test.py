from faker import Faker

from desk_reservation.seats.application.seat_creator import SeatCreator


def test__seat_creator__was_called_correctly(mocker, seat_factory):
    user_id=Faker().uuid4()
    seat = seat_factory()
    seat_service = mocker.Mock()
    seat_creator = SeatCreator(seat_service=seat_service)
    
    seat_creator.execute(seat=seat, user_id=user_id)
    
    seat_creator.seat_service.create_seat.assert_called_with(user_id=user_id, seat=seat)
   