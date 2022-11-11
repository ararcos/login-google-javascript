from desk_reservation.seats.application.seat_finder import SeatFinder



def test__seat_finder__was_called_correctly(mocker):
    criteria = mocker.Mock()
    seat_service = mocker.Mock()
    seat_updater = SeatFinder(seat_service=seat_service)
    
    seat_updater.execute(criteria=criteria)
    
    seat_updater.seat_service.find_seats.assert_called_with(criteria)