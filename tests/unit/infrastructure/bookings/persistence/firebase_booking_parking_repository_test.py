from typing import Callable, List
import pytest
from faker import Faker
from desk_reservation.bookings.infrastructure.persistence import (
    FirebaseBookingParkingRepository,
)
from desk_reservation.shared.infrastructure.firestore.firebase_repository import (
    FirebaseRepository,
)


@pytest.fixture(name="mocked_firebase_repository")
def _mocked_firebase(mocker) -> Callable:
    def _create_firebase_repository(collection_mocked: any) -> FirebaseRepository:
        firebase_mocked_instance = mocker.Mock(
            data_base=mocker.Mock(
                collection=mocker.Mock(return_value=collection_mocked)
            )
        )
        return firebase_mocked_instance

    return _create_firebase_repository


def test__create__return_booking_when_was_created(
    mocker, parking_booking_factory, mocked_firebase_repository
):
    booking = parking_booking_factory()
    firebase_reference = mocked_firebase_repository(mocker.Mock(document=mocker.Mock()))
    firebase_booking_repository = FirebaseBookingParkingRepository(firebase_reference)
    result = firebase_booking_repository.create(booking=booking)

    assert result == booking


def test__delete__return_true_when_was_deleted(mocker, mocked_firebase_repository):
    booking_id = Faker().uuid4()
    user_id = Faker().uuid4()

    firebase_reference = mocked_firebase_repository(
        mocker.Mock(
            document=mocker.Mock(
                return_value=mocker.Mock(
                    get=mocker.Mock(return_value=mocker.Mock(exists=True))
                )
            )
        )
    )

    firebase_booking_repository = FirebaseBookingParkingRepository(firebase_reference)
    result = firebase_booking_repository.delete(booking_id=booking_id, user_id=user_id)

    assert result is True


def test__delete__return_false_when_was_not_deleted(mocker, mocked_firebase_repository):
    booking_id = Faker().uuid4()
    user_id = Faker().uuid4()

    firebase_reference = mocked_firebase_repository(
        mocker.Mock(
            document=mocker.Mock(
                return_value=mocker.Mock(
                    get=mocker.Mock(return_value=mocker.Mock(exists=False))
                )
            )
        )
    )

    firebase_booking_repository = FirebaseBookingParkingRepository(firebase_reference)
    result = firebase_booking_repository.delete(booking_id=booking_id, user_id=user_id)

    assert result is False


def test__update__return_a_booking_when_it_is_updated(
    mocker, mocked_firebase_repository, parking_booking_factory
):
    booking_id = Faker().uuid4()
    update_by = Faker().uuid4()
    booking = parking_booking_factory()
    firebase_reference = mocked_firebase_repository(
        mocker.Mock(
            document=mocker.Mock(
                return_value=mocker.Mock(
                    get=mocker.Mock(return_value=mocker.Mock(exists=True))
                )
            )
        )
    )
    firebase_booking_repository = FirebaseBookingParkingRepository(firebase_reference)
    result = firebase_booking_repository.update(
        booking_id=booking_id, updated_by=update_by, booking=booking
    )

    assert result == booking


def test__update__return_a_none_when_it_is_not_updated(
    mocker, mocked_firebase_repository, parking_booking_factory
):
    booking_id = Faker().uuid4()
    update_by = Faker().uuid4()
    booking = parking_booking_factory()
    firebase_reference = mocked_firebase_repository(
        mocker.Mock(
            document=mocker.Mock(
                return_value=mocker.Mock(
                    get=mocker.Mock(return_value=mocker.Mock(exists=False))
                )
            )
        )
    )
    firebase_booking_repository = FirebaseBookingParkingRepository(firebase_reference)
    result = firebase_booking_repository.update(
        booking_id=booking_id, updated_by=update_by, booking=booking
    )

    assert result is None


def test__find__return_a_list_of_parking_bookings(
    mocker, mocked_firebase_repository, parking_booking_factory
):
    booking = parking_booking_factory()
    booking_dict = booking.__dict__
    reference_mocked = mocked_firebase_repository(mocker.Mock(
        get=mocker.Mock(
            return_value=[mocker.Mock(
                to_dict=mocker.Mock(
                    return_value=booking_dict),
                    id=booking.booking_id)])))

    firebase_repository = FirebaseBookingParkingRepository(reference_mocked)
    result = firebase_repository.find(mocker.Mock(filters=None))

    assert len(result) == 1
    assert booking in result


def test__find__return_empty_list_of_parking_bookings(mocker, mocked_firebase_repository):
    reference_mocked = mocked_firebase_repository(
        mocker.Mock(get=mocker.Mock(return_value=[]))
    )

    firebase_repository = FirebaseBookingParkingRepository(reference_mocked)
    result = firebase_repository.find(mocker.Mock(filters=None))

    assert len(result) == 0
    assert isinstance(result, List) is True
