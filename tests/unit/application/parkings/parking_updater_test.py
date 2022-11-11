from desk_reservation.parkings.application.parking_updater import ParkingUpdater


def test__parking_updater__was_called_correctly(mocker, parking_factory, user_factory):
    parking = parking_factory()
    user = user_factory()
    parking_service = mocker.Mock()
    parking_updater = ParkingUpdater(parking_service=parking_service)

    parking_updater.execute(user=user, parking=parking)

    parking_updater.parking_service.update_parking.assert_called_with(user_id=user.google_id, parking=parking)
