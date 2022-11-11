from faker import Faker

from desk_reservation.seats.application.seat_deleter import SeatDeleter



def test__seat_deleter__was_called_correctly(mocker, seat_factory):
    user_id=Faker().uuid4()
    office_id=Faker().uuid4()
    seat_id=Faker().uuid4()
    seat_service = mocker.Mock()
    seat_deleter = SeatDeleter(seat_service=seat_service)
    
    seat_deleter.execute(seat_id=seat_id, user_id=user_id, office_id=office_id)
    
    seat_deleter.seat_service.delete_seat.assert_called_with(user_id=user_id, office_id=office_id, seat_id=seat_id)
   