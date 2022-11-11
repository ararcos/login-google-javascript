from faker import Faker

from desk_reservation.parkings.application.parking_deleter import ParkingDeleter



def test__parking_deleter__was_called_correctly(mocker, user_factory):
    parking_id=Faker().uuid4()
    office_id = Faker().uuid4()
    parking_service = mocker.Mock()
    user = user_factory()
    parking_deleter = ParkingDeleter(parking_service=parking_service)
    
    parking_deleter.execute(parking_id=parking_id, user=user, office_id=office_id)
    
    parking_deleter.parking_service.delete_parking.assert_called_with(
        user_id=user.google_id, parking_id=parking_id, office_id=office_id)
   