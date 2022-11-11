from faker import Faker

from desk_reservation.parkings.application.parking_creator import ParkingCreator


def test__parking_creator__was_called_correctly(mocker, parking_factory, user_factory):
    parking = parking_factory()
    user_id = Faker().uuid4()
    parking_service = mocker.Mock()
    parking_creator = ParkingCreator(parking_service=parking_service)
    
    parking_creator.execute(parking=parking, user_id=user_id )
    
    parking_creator.parking_service.create_parking.assert_called_with(user_id=user_id, parking=parking)
   