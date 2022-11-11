import pytest
from faker import Faker

from desk_reservation.offices.application.office_creator import OfficeCreator



def test__return_true_when_office_is_created(mocker, office_factory):
    office = office_factory()
    office_service = mocker.Mock(
        create=mocker.Mock(return_value=office)
    )

    office_creator = OfficeCreator(office_service=office_service)
    result = office_creator.execute(office=office, user_id=Faker().uuid4())
    assert result == office