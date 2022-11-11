import pytest
from typing import Callable
from faker import Faker

from desk_reservation.offices.infrastructure.persistence.firebase_office_repository import (
    FirebaseOfficeRepository,
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


def test__return_office_when_office_is_created(
    mocked_firebase_repository, mocker, office_factory
):
    office = office_factory()
    firebase_mocked = mocked_firebase_repository(mocker.Mock())

    firebase_repository = FirebaseOfficeRepository(firebase_mocked)
    result = firebase_repository.create(office)
    assert result == office

def test__return_office_when_office_was_found(
    mocked_firebase_repository, mocker, office_factory
):
    office = office_factory().__dict__
    office_id = office.pop("office_id")
    firebase_mocked = mocked_firebase_repository(
        mocker.Mock(
            document=mocker.Mock(
                return_value=mocker.Mock(
                    get=mocker.Mock(
                        return_value=mocker.Mock(
                            id=office_id, to_dict=mocker.Mock(return_value=office)
                        )
                    ),
                    exists=True,
                )
            )
        )
    )
    firebase_repository = FirebaseOfficeRepository(firebase_mocked)

    result = firebase_repository.get(office_id)

    assert result.office_id == office_id


def test__return_None_when_office_was_not_found(
    mocked_firebase_repository, mocker, office_factory
):
    office = office_factory().__dict__
    office_id = office.pop("office_id")
    firebase_mocked = mocked_firebase_repository(
        mocker.Mock(
            document=mocker.Mock(
                return_value=mocker.Mock(
                    get=mocker.Mock(return_value=mocker.Mock(exists=False))
                )
            )
        )
    )
    firebase_repository = FirebaseOfficeRepository(firebase_mocked)

    result = firebase_repository.get(office_id)

    assert result == None


def test__return_list_of_office_when_db_has_data(
    mocked_firebase_repository, mocker, office_factory
):
    office = office_factory().__dict__
    office_id = office.pop("office_id")
    firebase_mocked = mocked_firebase_repository(
        mocker.Mock(
            get=mocker.Mock(
                return_value=[
                    mocker.Mock(to_dict=mocker.Mock(return_value=office), id=office_id)
                ]
            )
        )
    )
    firebase_repository = FirebaseOfficeRepository(firebase_mocked)

    result = firebase_repository.find(mocker.Mock(filters=None))

    assert len(result) == 1
    assert result[0].office_id == office_id


def test__return_empty_list_of_office_when_db_has_not_data(
    mocked_firebase_repository, mocker, office_factory
):
    firebase_mocked = mocked_firebase_repository(
        mocker.Mock(get=mocker.Mock(return_value=[]))
    )
    firebase_repository = FirebaseOfficeRepository(firebase_mocked)

    result = firebase_repository.find(mocker.Mock(filters=None))

    assert len(result) == 0
    assert result == []


def test__return_office_when_office_is_updated(
    mocked_firebase_repository, mocker, office_factory
):
    office = office_factory()
    firebase_mocked = mocked_firebase_repository(mocker.Mock())

    firebase_repository = FirebaseOfficeRepository(firebase_mocked)
    result = firebase_repository.update(office.office_id, office)
    assert result == office


def test__update_return_None_when_office_id_not_exist(
    mocked_firebase_repository, mocker, office_factory
):
    firebase_mocked = mocked_firebase_repository(
        mocker.Mock(
            document=mocker.Mock(
                return_value=mocker.Mock(
                    get=mocker.Mock(return_value=mocker.Mock(exists=False))
                )
            )
        )
    )
    firebase_repository = FirebaseOfficeRepository(firebase_mocked)

    result = firebase_repository.update(Faker().uuid4(), office_factory())
    assert result == None


def test__return_true_when_office_is_deleted(mocked_firebase_repository, mocker):
    firebase_mocked = mocked_firebase_repository(mocker.Mock())

    firebase_repository = FirebaseOfficeRepository(firebase_mocked)
    result = firebase_repository.delete(Faker().uuid4())
    assert result


def test__delete_return_None_when_office_id_not_exist(
    mocked_firebase_repository, mocker
):
    firebase_mocked = mocked_firebase_repository(
        mocker.Mock(
            document=mocker.Mock(
                return_value=mocker.Mock(
                    get=mocker.Mock(return_value=mocker.Mock(exists=False))
                )
            )
        )
    )
    firebase_repository = FirebaseOfficeRepository(firebase_mocked)

    result = firebase_repository.delete(Faker().uuid4())
    assert result is False
