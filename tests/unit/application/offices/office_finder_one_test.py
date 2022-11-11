import pytest

from faker import Faker

from desk_reservation.offices.application.office_finder_one import OfficeFinderOne


def test__find_an_office_when_id_no_exists(mocker):
    office_id = Faker().uuid4()
    office_service = mocker.Mock(
        get=mocker.Mock(return_value=None)
    )
    office_finder = OfficeFinderOne(office_service=office_service)

    result = office_finder.execute(office_id)
    assert result == None


def test__find_an_office_when_id_exist(mocker, office_factory):
    office_id = Faker().uuid4()
    office = office_factory(office_id=office_id)
    office_service = mocker.Mock(
        get=mocker.Mock(return_value=office)
    )

    office_finder = OfficeFinderOne(office_service=office_service)

    result = office_finder.execute(office_id=office_id)
    assert result.office_id == office_id
    assert result == office
