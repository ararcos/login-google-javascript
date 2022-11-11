from faker import Faker

from desk_reservation.parkings.application.parking_getter import ParkingGetter


def test__parking_getter__was_called_correctly(mocker, parking_factory):
    parking_id=Faker().uuid4()
    parking_service = mocker.Mock()
    parking_getter = ParkingGetter(parking_service=parking_service)
    
    parking_getter.execute(parking_id=parking_id)
    
    parking_getter.parking_service.get_parking_by_id.assert_called_with(parking_id=parking_id)
   