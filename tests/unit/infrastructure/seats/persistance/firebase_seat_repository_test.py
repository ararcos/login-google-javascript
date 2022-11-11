import pytest
from typing import Callable, List
from faker import Faker
from desk_reservation.seats.infrastructure.persistance.firebase_seat_repository import FirebaseSeatRepository
from desk_reservation.shared.infrastructure.firestore.firebase_repository import FirebaseRepository
from tests.unit._factories.seat_factory import seat_factory


@pytest.fixture(name='mocked_firebase_repository')
def _mocked_firebase(mocker) -> Callable:
    def _create_firebase_repository(collection_mocked: any) -> FirebaseRepository:
        firebase_mocked_instance = mocker.Mock(data_base=mocker.Mock(
            collection=mocker.Mock(return_value=collection_mocked)))
        return firebase_mocked_instance
    return _create_firebase_repository


def test__get__return_seat_when_was_found(mocker, mocked_firebase_repository, seat_factory):
    seat = seat_factory()
    seat_dict = seat.__dict__
    reference_mocked = mocked_firebase_repository(mocker.Mock(
        document=mocker.Mock(
            return_value=mocker.Mock(
                get=mocker.Mock(
                    return_value=mocker.Mock(
                        to_dict=mocker.Mock(
                            return_value=seat_dict),
                        exists=True))
            ))
        ))

    firebase_repository = FirebaseSeatRepository(reference_mocked)
    
    result = firebase_repository.get(seat.seat_id)
    assert result == seat

def test__get__return_None_when_seat_was_not_found(mocker, mocked_firebase_repository, seat_factory):
    seat = seat_factory()
    reference_mocked = mocked_firebase_repository(mocker.Mock(
        document=mocker.Mock(
            return_value=mocker.Mock(
                get=mocker.Mock(
                    return_value=mocker.Mock(
                        exists=False))
            ))
        ))

    firebase_repository = FirebaseSeatRepository(reference_mocked)
    
    result = firebase_repository.get(seat.seat_id)
    assert result == None


def test__find__return_list_of_seats_when_db_has_data(mocker, mocked_firebase_repository, seat_factory):
    seat = seat_factory()
    seat_dict = seat.__dict__
    reference_mocked = mocked_firebase_repository(mocker.Mock(
        get=mocker.Mock(
            return_value=[mocker.Mock(
                to_dict=mocker.Mock(
                    return_value=seat_dict))])))
    
    firebase_repository = FirebaseSeatRepository(reference_mocked)
    result = firebase_repository.find(mocker.Mock(filters=None))
    
    assert len(result) == 1
    assert seat in result
    

def test__find__return_empty_list_of_seats_when_db_has_not_data(mocker, mocked_firebase_repository):
    reference_mocked = mocked_firebase_repository(mocker.Mock(
        get=mocker.Mock(
            return_value=[])))
    
    firebase_repository = FirebaseSeatRepository(reference_mocked)
    result = firebase_repository.find(mocker.Mock(filters=None))
    
    assert len(result) == 0
    assert isinstance(result,List) == True
    
def test__update__return_seat_when_seat_was_updated(mocker, mocked_firebase_repository, seat_factory):
    seat = seat_factory()
    
    reference_mocked = mocked_firebase_repository(mocker.Mock(
        document=mocker.Mock(
            return_value=mocker.Mock(
                get=mocker.Mock(
                    return_value=mocker.Mock(
                        exists=True))
            )
            )))
    
    firebase_repository = FirebaseSeatRepository(reference_mocked)
    result = firebase_repository.update(seat=seat)
    
    assert result == seat
    

def test__update__return_None_when_seat_was_not_updated(mocker, mocked_firebase_repository, seat_factory):
    seat_id = Faker().uuid4()
    seat = seat_factory()
    
    reference_mocked = mocked_firebase_repository(mocker.Mock(
        document=mocker.Mock(
            return_value=mocker.Mock(
                get=mocker.Mock(
                    return_value=mocker.Mock(
                        exists=False))
            )
            )))
    
    firebase_repository = FirebaseSeatRepository(reference_mocked)
    result = firebase_repository.update(seat=seat)
    
    assert result == None
    
def test__create__return_seat_when_seat_was_created(mocker, mocked_firebase_repository, seat_factory):
    seat = seat_factory()
    
    reference_mocked = mocked_firebase_repository(mocker.Mock(
        document=mocker.Mock(
            return_value=mocker.Mock())))
    
    firebase_repository = FirebaseSeatRepository(reference_mocked)
    result = firebase_repository.create(seat)
    
    assert result == seat
    
def test__create_many__return_seats_when_seats_were_created(mocker, mocked_firebase_repository, seat_factory):
    seats = [seat_factory()]
    
    reference_mocked = mocked_firebase_repository(mocker.Mock())
    
    firebase_repository = FirebaseSeatRepository(reference_mocked)
    result = firebase_repository.create_many(seats)
    
    assert result == seats
    
    
def test__delete__return_True_when_seat_was_deleted(mocker, mocked_firebase_repository):
    seat_id = Faker().uuid4()
    
    reference_mocked = mocked_firebase_repository(mocker.Mock(
        document=mocker.Mock(
            return_value=mocker.Mock(
                get=mocker.Mock(
                    return_value=mocker.Mock(
                        exists=True))
                )
            )))
    
    firebase_repository = FirebaseSeatRepository(reference_mocked)
    result = firebase_repository.delete(seat_id=seat_id)
    
    assert result == True
    
    
def test__delete__return_False_when_seat_was_not_deleted(mocker, mocked_firebase_repository):
    seat_id = Faker().uuid4()
    
    reference_mocked = mocked_firebase_repository(mocker.Mock(
        document=mocker.Mock(
            return_value=mocker.Mock(
                get=mocker.Mock(
                    return_value=mocker.Mock(
                        exists=False))
                )
            )))
    
    firebase_repository = FirebaseSeatRepository(reference_mocked)
    result = firebase_repository.delete(seat_id=seat_id)
    
    assert result == False
