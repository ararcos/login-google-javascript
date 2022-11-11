from typing import Callable
from faker import Faker
import pytest

from desk_reservation.desks.infrastructure.persistence.firebase_desk_repository import (
    FirebaseDeskRepository,
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


def test__return_desk_when_desk_is_created(
    mocked_firebase_repository, mocker, desk_factory
):
    desk = desk_factory()
    firebase_mocked = mocked_firebase_repository(mocker.Mock())

    firebase_repository = FirebaseDeskRepository(firebase_mocked)
    result = firebase_repository.create(desk)
    assert result == desk


def test__return_desk_when_desk_was_found(
    mocked_firebase_repository, mocker, desk_factory
):
    desk = desk_factory().__dict__
    desk_id = desk.pop("desk_id")
    get_to_dict = mocker.Mock(return_value=desk)
    document_get = mocker.Mock(return_value=mocker.Mock(to_dict=get_to_dict,exists=True))
    document = mocker.Mock(return_value=mocker.Mock(get=document_get))
    firebase_mocked = mocked_firebase_repository(mocker.Mock(document=document))
    firebase_repository = FirebaseDeskRepository(firebase_mocked)

    result = firebase_repository.get(desk_id)

    assert result.desk_id == desk_id


def test__return_none_when_desk_was_not_found(
    mocked_firebase_repository, mocker, desk_factory
):
    desk = desk_factory().__dict__
    desk_id = desk.pop("desk_id")
    get_to_dict = mocker.Mock(return_value=desk)
    document_get = mocker.Mock(return_value=mocker.Mock(to_dict=get_to_dict,exists=False))
    document = mocker.Mock(return_value=mocker.Mock(get=document_get))
    firebase_mocked = mocked_firebase_repository(mocker.Mock(document=document))

    firebase_repository = FirebaseDeskRepository(firebase_mocked)

    result = firebase_repository.get(desk_id)

    assert result is None


def test__return_list_of_desk_when_db_has_data(
    mocked_firebase_repository, mocker, desk_factory
):
    desk = desk_factory().__dict__
    desk_id = desk.pop("desk_id")
    get_to_dict = mocker.Mock(return_value=desk)
    fb_get = mocker.Mock(return_value=[mocker.Mock(to_dict=get_to_dict, id=desk_id)])
    fire_base = mocker.Mock(get=fb_get)
    firebase_mocked = mocked_firebase_repository(fire_base)
    firebase_repository = FirebaseDeskRepository(firebase_mocked)

    result = firebase_repository.find(mocker.Mock(filters=None))

    assert len(result) == 1
    assert result[0].desk_id == desk_id


def test__return_empty_list_of_desk_when_db_has_not_data(
    mocked_firebase_repository, mocker
):
    firebase_mocked = mocked_firebase_repository(
        mocker.Mock(get=mocker.Mock(return_value=[]))
    )
    firebase_repository = FirebaseDeskRepository(firebase_mocked)

    result = firebase_repository.find(mocker.Mock(filters=None))

    assert len(result) == 0
    assert result == []


def test__return_desk_when_desk_is_updated(
    mocked_firebase_repository, mocker, desk_factory
):
    desk = desk_factory()
    firebase_mocked = mocked_firebase_repository(mocker.Mock())

    firebase_repository = FirebaseDeskRepository(firebase_mocked)
    result = firebase_repository.update(desk.desk_id, desk)
    assert result == desk


def test__update_return_none_when_desk_id_not_exist(
    mocked_firebase_repository, mocker, desk_factory
):
    desk = desk_factory()
    get_to_dict = mocker.Mock(return_value=desk)
    document_get = mocker.Mock(return_value=mocker.Mock(to_dict=get_to_dict,exists=False))
    document = mocker.Mock(return_value=mocker.Mock(get=document_get))
    firebase_mocked = mocked_firebase_repository(mocker.Mock(document=document))
    firebase_repository = FirebaseDeskRepository(firebase_mocked)

    result = firebase_repository.update(Faker().uuid4(), desk_factory())
    assert result is None


def test__return_true_when_desk_is_deleted(mocked_firebase_repository, mocker):
    firebase_mocked = mocked_firebase_repository(mocker.Mock())

    firebase_repository = FirebaseDeskRepository(firebase_mocked)
    user_id = Faker().uuid4()
    desk_id = Faker().uuid4()
    result = firebase_repository.delete(user_id,desk_id)
    assert result


def test__delete_return_none_when_desk_id_not_exist(
    mocked_firebase_repository, mocker, desk_factory
    ):
    desk = desk_factory()
    get_to_dict = mocker.Mock(return_value=desk)
    document_get = mocker.Mock(return_value=mocker.Mock(to_dict=get_to_dict,exists=False))
    document = mocker.Mock(return_value=mocker.Mock(get=document_get))
    firebase_mocked = mocked_firebase_repository(mocker.Mock(document=document))
    firebase_repository = FirebaseDeskRepository(firebase_mocked)
    user_id = Faker().uuid4()
    desk_id = Faker().uuid4()
    result = firebase_repository.delete(user_id,desk_id)
    assert result is False
