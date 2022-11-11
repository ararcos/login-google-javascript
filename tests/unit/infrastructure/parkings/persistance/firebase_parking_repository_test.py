import pytest
from typing import Callable, List
from faker import Faker
from desk_reservation.parkings.infrastructure.persistence.firebase_parking_repository import FirebaseParkingRepository
from desk_reservation.shared.infrastructure.firestore.firebase_repository import FirebaseRepository
from tests.unit._factories.parking_factory import parking_factory


@pytest.fixture(name='mocked_firebase_repository')
def _mocked_firebase(mocker) -> Callable:
    def _create_firebase_repository(collection_mocked: any) -> FirebaseRepository:
        firebase_mocked_instance = mocker.Mock(data_base=mocker.Mock(
            collection=mocker.Mock(return_value=collection_mocked)))
        return firebase_mocked_instance
    return _create_firebase_repository


def test__get__return_parking_when_was_found(mocker, mocked_firebase_repository, parking_factory):
    parking = parking_factory()
    parking_dict = parking.__dict__
    reference_mocked = mocked_firebase_repository(mocker.Mock(
        document=mocker.Mock(
            return_value=mocker.Mock(
                get=mocker.Mock(
                    return_value=mocker.Mock(
                        to_dict=mocker.Mock(
                            return_value=parking_dict),
                        exists=True))
            ))
    ))

    firebase_repository = FirebaseParkingRepository(reference_mocked)

    result = firebase_repository.get(parking.parking_id)
    assert result == parking


def test__get__return_None_when_parking_was_not_found(mocker, mocked_firebase_repository, parking_factory):
    parking = parking_factory()
    reference_mocked = mocked_firebase_repository(mocker.Mock(
        document=mocker.Mock(
            return_value=mocker.Mock(
                get=mocker.Mock(
                    return_value=mocker.Mock(
                        exists=False))
            ))
    ))

    firebase_repository = FirebaseParkingRepository(reference_mocked)

    result = firebase_repository.get(parking.parking_id)
    assert result == None


def test__find__return_list_of_parkings_when_db_has_data(mocker, mocked_firebase_repository, parking_factory):
    parking = parking_factory()
    parking_dict = parking.__dict__
    reference_mocked = mocked_firebase_repository(mocker.Mock(
        get=mocker.Mock(
            return_value=[mocker.Mock(
                to_dict=mocker.Mock(
                    return_value=parking_dict))])))

    firebase_repository = FirebaseParkingRepository(reference_mocked)
    result = firebase_repository.find(mocker.Mock(filters=None))

    assert len(result) == 1
    assert parking in result


def test__find__return_empty_list_of_parkings_when_db_has_not_data(mocker, mocked_firebase_repository):
    reference_mocked = mocked_firebase_repository(mocker.Mock(
        get=mocker.Mock(
            return_value=[])))

    firebase_repository = FirebaseParkingRepository(reference_mocked)
    result = firebase_repository.find(mocker.Mock(filters=None))

    assert len(result) == 0
    assert isinstance(result, List) == True


def test__update__return_parking_when_parking_was_updated(mocker, mocked_firebase_repository, parking_factory):
    parking = parking_factory()

    reference_mocked = mocked_firebase_repository(mocker.Mock(
        document=mocker.Mock(
            return_value=mocker.Mock(
                get=mocker.Mock(
                    return_value=mocker.Mock(
                        exists=True))
            )
        )))

    firebase_repository = FirebaseParkingRepository(reference_mocked)
    result = firebase_repository.update(parking=parking)

    assert result == parking


def test__update__return_None_when_parking_was_not_updated(mocker, mocked_firebase_repository, parking_factory):
    parking_id = Faker().uuid4()
    parking = parking_factory()

    reference_mocked = mocked_firebase_repository(mocker.Mock(
        document=mocker.Mock(
            return_value=mocker.Mock(
                get=mocker.Mock(
                    return_value=mocker.Mock(
                        exists=False))
            )
        )))

    firebase_repository = FirebaseParkingRepository(reference_mocked)
    result = firebase_repository.update(parking=parking)

    assert result == None


def test__create__return_parking_when_parking_was_created(mocker, mocked_firebase_repository, parking_factory):
    parking = parking_factory()

    reference_mocked = mocked_firebase_repository(mocker.Mock(
        document=mocker.Mock(
            return_value=mocker.Mock())))

    firebase_repository = FirebaseParkingRepository(reference_mocked)
    result = firebase_repository.create(parking)

    assert result == parking


def test__delete__return_True_when_parking_was_deleted(mocker, mocked_firebase_repository):
    parking_id = Faker().uuid4()

    reference_mocked = mocked_firebase_repository(mocker.Mock(
        document=mocker.Mock(
            return_value=mocker.Mock(
                get=mocker.Mock(
                    return_value=mocker.Mock(
                        exists=True))
            )
        )))

    firebase_repository = FirebaseParkingRepository(reference_mocked)
    result = firebase_repository.delete(parking_id=parking_id)

    assert result == True


def test__delete__return_False_when_parking_was_not_deleted(mocker, mocked_firebase_repository):
    parking_id = Faker().uuid4()

    reference_mocked = mocked_firebase_repository(mocker.Mock(
        document=mocker.Mock(
            return_value=mocker.Mock(
                get=mocker.Mock(
                    return_value=mocker.Mock(
                        exists=False))
            )
        )))

    firebase_repository = FirebaseParkingRepository(reference_mocked)
    result = firebase_repository.delete(parking_id=parking_id)

    assert result == False
