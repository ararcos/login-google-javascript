from typing import Callable
from faker import Faker
import pytest
from desk_reservation.ride.infrastructure.persistance.firebase_ride_repository import (
    FirebaseRideRepository,
)
from desk_reservation.shared.domain.exceptions.bad_request import BadRequestError

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


def test__return_ride_when_ride_is_created(
    mocked_firebase_repository, mocker, ride_factory
):
    ride = ride_factory()
    firebase_mocked = mocked_firebase_repository(mocker.Mock())

    firebase_repository = FirebaseRideRepository(firebase_mocked)
    result = firebase_repository.create(ride)
    assert result == ride


def test__return_bad_request_error_when_ride_dont_have_ride_id(
    mocked_firebase_repository, mocker, ride_factory
):
    ride = ride_factory()
    ride.__dict__.pop("ride_id")
    firebase_mocked = mocked_firebase_repository(mocker.Mock())

    firebase_repository = FirebaseRideRepository(firebase_mocked)
    with pytest.raises(BadRequestError):
        firebase_repository.create(ride)


def test__return_ride_when_ride_was_found(
    mocked_firebase_repository, mocker, ride_factory
):
    ride = ride_factory().__dict__
    ride_id = ride.pop("ride_id")
    get_to_dict = mocker.Mock(return_value=ride)
    document_get = mocker.Mock(
        return_value=mocker.Mock(to_dict=get_to_dict, exists=True)
    )
    document = mocker.Mock(return_value=mocker.Mock(get=document_get))
    firebase_mocked = mocked_firebase_repository(
        mocker.Mock(document=document))
    firebase_repository = FirebaseRideRepository(firebase_mocked)

    result = firebase_repository.find_by_id(ride_id)

    assert result.ride_id == ride_id


def test__return_none_when_ride_was_not_found(
    mocked_firebase_repository, mocker, ride_factory
):
    ride = ride_factory().__dict__
    ride_id = ride.pop("ride_id")
    get_to_dict = mocker.Mock(return_value=ride)
    document_get = mocker.Mock(
        return_value=mocker.Mock(to_dict=get_to_dict, exists=False)
    )
    document = mocker.Mock(return_value=mocker.Mock(get=document_get))
    firebase_mocked = mocked_firebase_repository(
        mocker.Mock(document=document))

    firebase_repository = FirebaseRideRepository(firebase_mocked)

    result = firebase_repository.find_by_id(ride_id)

    assert result is None


def test__return_list_of_ride_when_db_has_data(
    mocked_firebase_repository, mocker, ride_factory
):
    ride = ride_factory().__dict__
    ride_id = ride.pop("ride_id")
    get_to_dict = mocker.Mock(return_value=ride)
    fb_get = mocker.Mock(
        return_value=[mocker.Mock(to_dict=get_to_dict, id=ride_id)])
    fire_base = mocker.Mock(get=fb_get)
    firebase_mocked = mocked_firebase_repository(fire_base)
    firebase_repository = FirebaseRideRepository(firebase_mocked)

    result = firebase_repository.find_all(mocker.Mock(filters=None))

    assert len(result) == 1
    assert result[0].ride_id == ride_id


def test__return_empty_list_of_ride_when_db_has_not_data(
    mocked_firebase_repository, mocker
):
    firebase_mocked = mocked_firebase_repository(
        mocker.Mock(get=mocker.Mock(return_value=[]))
    )
    firebase_repository = FirebaseRideRepository(firebase_mocked)

    result = firebase_repository.find_all(mocker.Mock(filters=None))

    assert len(result) == 0
    assert result == []


def test__return_ride_when_ride_is_updated(
    mocked_firebase_repository, mocker, ride_factory
):
    user_id = Faker().uuid4()
    ride_id = Faker().uuid4()
    ride = ride_factory()
    firebase_mocked = mocked_firebase_repository(mocker.Mock())

    firebase_repository = FirebaseRideRepository(firebase_mocked)
    result = firebase_repository.update(user_id, ride_id, ride)
    assert result == ride


def test__update_return_none_when_ride_id_not_exist(
    mocked_firebase_repository, mocker, ride_factory
):
    user_id = Faker().uuid4()
    ride_id = Faker().uuid4()
    ride = ride_factory()
    get_to_dict = mocker.Mock(return_value=ride)
    document_get = mocker.Mock(
        return_value=mocker.Mock(to_dict=get_to_dict, exists=False)
    )
    document = mocker.Mock(return_value=mocker.Mock(get=document_get))
    firebase_mocked = mocked_firebase_repository(
        mocker.Mock(document=document))
    firebase_repository = FirebaseRideRepository(firebase_mocked)

    result = firebase_repository.update(user_id, ride_id, ride)
    assert result is None


def test__return_true_when_ride_is_deleted(mocked_firebase_repository, mocker):
    firebase_mocked = mocked_firebase_repository(mocker.Mock())

    firebase_repository = FirebaseRideRepository(firebase_mocked)
    ride_id = Faker().uuid4()

    result = firebase_repository.delete(ride_id)

    assert result


def test__delete_return_none_when_ride_id_not_exist(
    mocked_firebase_repository, mocker, ride_factory
):
    ride = ride_factory()
    get_to_dict = mocker.Mock(return_value=ride)
    document_get = mocker.Mock(
        return_value=mocker.Mock(to_dict=get_to_dict, exists=False)
    )
    document = mocker.Mock(return_value=mocker.Mock(get=document_get))
    firebase_mocked = mocked_firebase_repository(
        mocker.Mock(document=document))
    firebase_repository = FirebaseRideRepository(firebase_mocked)
    ride_id = Faker().uuid4()

    result = firebase_repository.delete(ride_id)

    assert result is False


def test__booking_ride_return_booking_ride_when_is_created_correctly(
    mocked_firebase_repository, mocker, ride_booking_factory, ride_factory
):
    ride = ride_factory()
    ride_booking = ride_booking_factory()
    document_set = mocker.Mock(
        return_value=mocker.Mock(id=ride_booking.ride_booking_id)
    )
    document = mocker.Mock(return_value=mocker.Mock(set=document_set))
    firebase_mocked = mocked_firebase_repository(
        mocker.Mock(document=document))
    firebase_repository = FirebaseRideRepository(firebase_mocked)
    firebase_repository.find_by_id = mocker.Mock(return_value=ride)

    result = firebase_repository.booking_ride(ride_booking=ride_booking)

    assert result == ride_booking
    assert firebase_repository.find_by_id.called


def test__booking_ride_return_none_when_dont_exist_the_ride(
    mocked_firebase_repository, mocker, ride_booking_factory, ride_factory
):
    ride_booking = ride_booking_factory()
    firebase_mocked = mocked_firebase_repository(mocker.Mock())
    firebase_repository = FirebaseRideRepository(firebase_mocked)
    firebase_repository.find_by_id = mocker.Mock(return_value=None)

    result = firebase_repository.booking_ride(ride_booking=ride_booking)

    assert firebase_repository.find_by_id.called
    assert result is None


def test__booking_ride_raise_bad_request_error_when_dont_have_ride_booking_id(
    mocked_firebase_repository, mocker, ride_booking_factory, ride_factory
):
    ride = ride_factory()
    ride_booking = ride_booking_factory()
    ride_booking.__dict__.pop("ride_booking_id")
    firebase_mocked = mocked_firebase_repository(mocker.Mock())
    firebase_repository = FirebaseRideRepository(firebase_mocked)
    firebase_repository.find_by_id = mocker.Mock(return_value=ride)


    with pytest.raises(BadRequestError):
        firebase_repository.booking_ride(ride_booking=ride_booking)
        assert firebase_repository.find_by_id.called


def test__find_booking_ride_return_list_when_db_has_data(
    mocked_firebase_repository, mocker, ride_booking_factory
):
    ride_booking = ride_booking_factory().__dict__
    ride_booking_id = ride_booking.pop("ride_booking_id")
    get_to_dict = mocker.Mock(return_value=ride_booking)
    fb_get = mocker.Mock(
        return_value=[mocker.Mock(to_dict=get_to_dict, id=ride_booking_id)])
    fire_base = mocker.Mock(get=fb_get)
    firebase_mocked = mocked_firebase_repository(fire_base)
    firebase_repository = FirebaseRideRepository(firebase_mocked)

    result = firebase_repository.find_booking_ride(mocker.Mock(filters=None))

    assert len(result) == 1
    assert result[0].ride_booking_id == ride_booking_id


def test__find_booking_ride_return_empty_list_when_db_has_not_data(
    mocked_firebase_repository, mocker
):
    firebase_mocked = mocked_firebase_repository(
        mocker.Mock(get=mocker.Mock(return_value=[]))
    )
    firebase_repository = FirebaseRideRepository(firebase_mocked)

    result = firebase_repository.find_booking_ride(mocker.Mock(filters=None))

    assert len(result) == 0
    assert result == []


def test__find_by_id_booking_ride_return_ride_booking_when_id_exist(
    mocked_firebase_repository, mocker, ride_booking_factory
):
    ride_booking = ride_booking_factory().__dict__
    get_to_dict = mocker.Mock(return_value=ride_booking)
    document_get = mocker.Mock(
        return_value=mocker.Mock(to_dict=get_to_dict, exists=True)
    )
    document = mocker.Mock(return_value=mocker.Mock(get=document_get))
    firebase_mocked = mocked_firebase_repository(
        mocker.Mock(document=document))
    firebase_repository = FirebaseRideRepository(firebase_mocked)

    result = firebase_repository.find_by_id_booking_ride(ride_booking["ride_booking_id"])

    assert result == ride_booking


def test__find_by_id_booking_ride_return_empty_list_when_db_has_not_data(
    mocked_firebase_repository, mocker
):
    document_get = mocker.Mock(
        return_value=mocker.Mock(exists=False)
    )
    document = mocker.Mock(return_value=mocker.Mock(get=document_get))
    firebase_mocked = mocked_firebase_repository(
        mocker.Mock(document=document))
    firebase_repository = FirebaseRideRepository(firebase_mocked)

    result = firebase_repository.find_by_id_booking_ride(Faker().uuid4())

    assert result is None
