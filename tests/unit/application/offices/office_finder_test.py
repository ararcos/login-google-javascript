import pytest
from faker import Faker

from desk_reservation.offices.application import OfficeFinder


def test__find_offices_when_data_exists(mocker, office_factory):
    offices = [office_factory() for _ in range(3)]
    criteria = mocker.Mock()
    office_service = mocker.Mock(
        find=mocker.Mock(return_value=offices)
    )

    office_finder = OfficeFinder(office_service=office_service)

    result = office_finder.execute(criteria=criteria, populate=False)
    assert result == offices


def test__find_offices_when_data_no_exist(mocker):
    criteria = mocker.Mock()
    office_service = mocker.Mock(
        find=mocker.Mock(return_value=[])
    )

    office_finder = OfficeFinder(office_service=office_service)

    result = office_finder.execute(criteria=criteria, populate=False)
    assert result == []
