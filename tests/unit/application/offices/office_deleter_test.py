import pytest
from faker import Faker

from desk_reservation.offices.application import OfficeDeleter


def test__find_raise_an_exception_when_office_cannot_be_deleted(mocker):
    office_id = Faker().uuid4()
    user_id = Faker().uuid4()
    office_service = mocker.Mock(
        delete=mocker.Mock(return_value=False)
    )
    office_deleter = OfficeDeleter(office_service=office_service)

    result = office_deleter.execute(office_id=office_id, user_id=user_id)
    assert result == False


def test__return_true_when_office_is_deleted(mocker):
    office_id = Faker().uuid4()
    user_id = Faker().uuid4()
    office_service = mocker.Mock(
        delete=mocker.Mock(return_value=True)
    )

    office_deleter = OfficeDeleter(office_service=office_service)
    result = office_deleter.execute(office_id=office_id, user_id=user_id)
    assert result == True
