from typing import Callable, List
import pytest
from faker import Faker

from desk_reservation.shared.domain.exceptions.bad_request import BadRequestError
from desk_reservation.shared.infrastructure.firestore.firebase_repository import FirebaseRepository
from desk_reservation.users.infrastructure.persistence.firebase_user_repository import FirebaseUserRepository


@pytest.fixture(name='mocked_firebase_repository')
def _mocked_firebase(mocker) -> Callable:
    def _create_firebase_repository(collection_mocked: any) -> FirebaseRepository:
        firebase_mocked_instance = mocker.Mock(data_base=mocker.Mock(
            collection=mocker.Mock(return_value=collection_mocked)))
        return firebase_mocked_instance
    return _create_firebase_repository


def test__return_user_when_user_is_created(mocked_firebase_repository, mocker, user_factory):
    user = user_factory()
    firebase_mocked = mocked_firebase_repository(mocker.Mock())

    firebase_repository = FirebaseUserRepository(firebase_mocked)
    result = firebase_repository.create(user)
    assert result == user


def test__return_error_when_user_dont_exist(mocked_firebase_repository, mocker):
    firebase_mocked = mocked_firebase_repository(mocker.Mock(
        document=mocker.Mock(
            return_value=mocker.Mock(
                get=mocker.Mock(
                    return_value=mocker.Mock(
                        exists=False
                    )
                )
            )
        )
    ))
    firebase_repository = FirebaseUserRepository(firebase_mocked)
    result = firebase_repository.get(Faker().uuid4())
    assert result is None


def test__return_user_when_user_was_found(mocked_firebase_repository, mocker, user_factory):
    user = user_factory()
    google_id = user.google_id
    firebase_mocked = mocked_firebase_repository(mocker.Mock(
        document=mocker.Mock(
            return_value=mocker.Mock(
                exists=True,
                get=mocker.Mock(
                    return_value=mocker.Mock(
                        to_dict=mocker.Mock(
                            return_value= user.__dict__
                            )
                    )
                )
            )
        )
    ))
    firebase_repository = FirebaseUserRepository(firebase_mocked)
    result = firebase_repository.get(google_id)
    assert result == user


def test__find__return_list_of_users_when_db_has_data(mocker, mocked_firebase_repository, user_factory):
    user = user_factory()
    user_dict = user.__dict__
    reference_mocked = mocked_firebase_repository(mocker.Mock(
        get=mocker.Mock(
            return_value=[mocker.Mock(
                to_dict=mocker.Mock(
                    return_value=user_dict))])))
    
    firebase_repository = FirebaseUserRepository(reference_mocked)
    result = firebase_repository.find(mocker.Mock(filters=None))
    
    assert len(result) == 1
    assert user in result


def test__find__return_empty_list_of_users_when_db_has_not_data(mocker, mocked_firebase_repository):
    reference_mocked = mocked_firebase_repository(mocker.Mock(
        get=mocker.Mock(
            return_value=[])))
    
    firebase_repository = FirebaseUserRepository(reference_mocked)
    result = firebase_repository.find(mocker.Mock(filters=None))
    
    assert len(result) == 0
    assert isinstance(result,List) == True


def test__update__return_user_when_user_was_updated(mocker, mocked_firebase_repository, user_factory):
    user = user_factory()
    google_id = Faker().uuid4()
    reference_mocked = mocked_firebase_repository(mocker.Mock(
        document=mocker.Mock(
            return_value=mocker.Mock(
                exists=True)
            )))
    
    firebase_repository = FirebaseUserRepository(reference_mocked)
    result = firebase_repository.edit(google_id=google_id, user=user)
    
    assert result == user


def test__update__return_None_when_user_was_not_updated(mocker, mocked_firebase_repository, user_factory):
    user = user_factory()
    google_id = Faker().uuid4()
    firebase_mocked = mocked_firebase_repository(mocker.Mock(
        document=mocker.Mock(
            return_value=mocker.Mock(
                get=mocker.Mock(
                    return_value=mocker.Mock(
                        exists=False
                    )
                )
            )
        )
    ))
    firebase_repository = FirebaseUserRepository(firebase_mocked)
    result = firebase_repository.edit(google_id=google_id, user=user)
    
    assert result == None


def test__delete__return_True_when_user_was_deleted(mocker, mocked_firebase_repository):
    google_id= Faker().uuid4()
    reference_mocked = mocked_firebase_repository(mocker.Mock(
        document=mocker.Mock(
            return_value=mocker.Mock(
                exists=True)
            )))
    
    firebase_repository = FirebaseUserRepository(reference_mocked)
    result = firebase_repository.delete(google_id=google_id)
    
    assert result == True


def test__delete__return_False_when_user_was_not_deleted(mocker, mocked_firebase_repository):
    google_id= Faker().uuid4()
    firebase_mocked = mocked_firebase_repository(mocker.Mock(
        document=mocker.Mock(
            return_value=mocker.Mock(
                get=mocker.Mock(
                    return_value=mocker.Mock(
                        exists=False
                    )
                )
            )
        )
    ))
    firebase_repository = FirebaseUserRepository(firebase_mocked)
    result = firebase_repository.delete(google_id=google_id)
    
    assert result == False