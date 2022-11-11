import json
from typing import Callable, List
import pytest
from faker import Faker
from desk_reservation.bookings.infrastructure.persistence.firebase_booking_repository import FirebaseBookingRepository
from desk_reservation.shared.infrastructure.firestore.firebase_repository import FirebaseRepository

@pytest.fixture(name='mocked_firebase_repository')
def _mocked_firebase(mocker) -> Callable:
    def _create_firebase_repository(collection_mocked: any) -> FirebaseRepository:
        firebase_mocked_instance = mocker.Mock(data_base=mocker.Mock(
            collection=mocker.Mock(return_value=collection_mocked)))
        return firebase_mocked_instance
    return _create_firebase_repository

def test__create__return_booking_when_was_created(
        mocker,
        seat_booking_factory,
        mocked_firebase_repository
    ):
    booking = seat_booking_factory()
    firebase_reference = mocked_firebase_repository(mocker.Mock(document=mocker.Mock()))
    firebase_booking_repository = FirebaseBookingRepository(firebase_reference)
    result = firebase_booking_repository.create(booking=booking)

    assert result == booking

def test__create_many__return_bookings(mocker, mocked_firebase_repository, seat_booking_factory):
    bookings = [seat_booking_factory()]

    reference_mocked = mocked_firebase_repository(mocker.Mock())

    firebase_repository = FirebaseBookingRepository(reference_mocked)
    result = firebase_repository.create_many(bookings)

    assert result == bookings

def test__get__return_booking_when_was_found(
        mocker,
        seat_booking_factory,
        mocked_firebase_repository
    ):
    booking_id = Faker().uuid4()
    booking = seat_booking_factory().__dict__
    firebase_reference = mocked_firebase_repository(mocker.Mock(
        document=mocker.Mock(return_value=mocker.Mock(
            get=mocker.Mock(return_value=mocker.Mock(
                exists=True,
                to_dict=mocker.Mock(return_value=booking)
            ))
        ))
    ))
    firebase_booking_repository = FirebaseBookingRepository(firebase_reference)
    result = firebase_booking_repository.get(booking_id=booking_id)

    assert result == booking

def test__get__return_none_when_was_not_found(mocker, mocked_firebase_repository):
    booking_id = Faker().uuid4()
    firebase_reference = mocked_firebase_repository(mocker.Mock(
        document=mocker.Mock(return_value=mocker.Mock(
            get=mocker.Mock(return_value=mocker.Mock(
                exists=False,
            ))
        ))
    ))

    firebase_booking_repository = FirebaseBookingRepository(firebase_reference)
    result = firebase_booking_repository.get(booking_id=booking_id)

    assert result is None

def test__delete__return_true_when_was_deleted(mocker, mocked_firebase_repository):
    booking_id=Faker().uuid4()
    user_id=Faker().uuid4()


    firebase_reference = mocked_firebase_repository(mocker.Mock(
        document=mocker.Mock(
            return_value=mocker.Mock(
                get=mocker.Mock(
                    return_value=mocker.Mock(
                        exists=True
                        ))))))

    firebase_booking_repository = FirebaseBookingRepository(firebase_reference)
    result = firebase_booking_repository.delete(booking_id=booking_id, user_id=user_id)

    assert result is True

def test__delete__return_false_when_was_not_deleted(mocker, mocked_firebase_repository):
    booking_id=Faker().uuid4()
    user_id=Faker().uuid4()

    firebase_reference = mocked_firebase_repository(mocker.Mock(
        document=mocker.Mock(
            return_value=mocker.Mock(
                get=mocker.Mock(
                    return_value=mocker.Mock(
                        exists=False
                        ))))))

    firebase_booking_repository = FirebaseBookingRepository(firebase_reference)
    result = firebase_booking_repository.delete(booking_id=booking_id, user_id=user_id)

    assert result is False

def test__update__return_a_booking_when_it_is_updated(
        mocker,
        mocked_firebase_repository,
        seat_booking_factory
    ):
    booking_id = Faker().uuid4()
    update_by = Faker().uuid4()
    booking = seat_booking_factory()
    firebase_reference = mocked_firebase_repository(mocker.Mock(
        document=mocker.Mock(
            return_value=mocker.Mock(
                get=mocker.Mock(
                    return_value=mocker.Mock(
                        exists=True
                    ))))))
    firebase_booking_repository = FirebaseBookingRepository(firebase_reference)
    result = firebase_booking_repository.update(
            booking_id=booking_id,
            updated_by=update_by,
            booking=booking
        )

    assert result == booking

def test__update__return_a_none_when_it_is_not_updated(
        mocker,
        mocked_firebase_repository,
        seat_booking_factory
    ):
    booking_id = Faker().uuid4()
    update_by = Faker().uuid4()
    booking = seat_booking_factory()
    firebase_reference = mocked_firebase_repository(mocker.Mock(
        document=mocker.Mock(
            return_value=mocker.Mock(
                get=mocker.Mock(
                    return_value=mocker.Mock(
                        exists=False
                    ))))))
    firebase_booking_repository = FirebaseBookingRepository(firebase_reference)
    result = firebase_booking_repository.update(
            booking_id=booking_id,
            updated_by=update_by,
            booking=booking
        )

    assert result is None

def test__find__return_a_list_of_bookings(mocker, mocked_firebase_repository, seat_booking_factory):
    booking = seat_booking_factory()
    booking_dict = booking.__dict__
    reference_mocked = mocked_firebase_repository(mocker.Mock(
        get=mocker.Mock(
            return_value=[mocker.Mock(
                to_dict=mocker.Mock(
                    return_value=booking_dict),
                    id=booking.booking_id)])))

    firebase_repository = FirebaseBookingRepository(reference_mocked)
    result = firebase_repository.find(mocker.Mock(filters=None))

    assert len(result) == 1

def test__find__return_empty_list_of_bookings(mocker, mocked_firebase_repository):
    reference_mocked = mocked_firebase_repository(mocker.Mock(
        get=mocker.Mock(
            return_value=[])))

    firebase_repository = FirebaseBookingRepository(reference_mocked)
    result = firebase_repository.find(mocker.Mock(filters=None))

    assert len(result) == 0
    assert isinstance(result,List) is True
