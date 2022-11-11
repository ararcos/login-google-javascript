from desk_reservation.parkings.application.parking_finder import ParkingFinder



def test__parking_finder__was_called_correctly(mocker):
    criteria = mocker.Mock()
    parking_service = mocker.Mock()
    parking_updater = ParkingFinder(parking_service=parking_service)
    
    parking_updater.execute(criteria=criteria)
    
    parking_updater.parking_service.find_parkings.assert_called_with(criteria=criteria)