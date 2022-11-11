from faker import Faker

from desk_reservation.seats.application.seat_updater import SeatUpdater


def test__seat_updater__was_called_correctly(mocker, seat_factory):
    user_id = Faker().uuid4()
    seat = seat_factory()

    seat_service = mocker.Mock()
    seat_updater = SeatUpdater(seat_service=seat_service)

    seat_updater.execute(user_id=user_id, seat=seat)

    seat_updater.seat_service.update_seat.assert_called_with(seat=seat, user_id=user_id)
