import pytest
from faker import Faker

from desk_reservation.offices.application.office_updater import OfficeUpdater


def test__update_an_office_when_office_id_not_exist(mocker, office_factory):
    office_id = Faker().uuid4()
    user_id = Faker().uuid4()
    office = office_factory(office_id=office_id)
    office_service = mocker.Mock(
        update=mocker.Mock(return_value=None)
    )
    office_updater = OfficeUpdater(office_service=office_service)

    result = office_updater.execute(office=office, office_id=office_id, user_id=user_id)
    assert result == None
