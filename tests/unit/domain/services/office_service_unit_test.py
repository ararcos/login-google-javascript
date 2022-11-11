import pytest
from faker import Faker

from desk_reservation.offices.domain import OfficeService


@pytest.fixture(name='dependencies')
def _service_dependencies(mocker):
    seat_repository = mocker.Mock()
    parking_repository = mocker.Mock()
    office_repository = mocker.Mock()
    user_repository = mocker.Mock()
    office_service = OfficeService(
        seat_repository=seat_repository, parking_repository=parking_repository, office_repository=office_repository, user_repository=user_repository
    )
    office_service._has_permissions = mocker.Mock(return_value=True)
    return {
        'office_repository': office_repository,
        'parking_repository': parking_repository,
        'seat_repository': seat_repository,
        'service': office_service,
    }


def test__create_office__was_called_correctly(dependencies, mocker, office_factory):
    office_repository, parking_repository, seat_repository, service = dependencies.values()
    office = office_factory()
    office_repository.create = mocker.Mock(return_value=office)

    result = service.create(office, Faker().uuid4())

    office_repository.create.assert_called_with(office)
    assert result == office


def test__update_office__was_called_correctly(dependencies, mocker, office_factory):
    office_repository, parking_repository, seat_repository, service = dependencies.values()
    office = office_factory()
    office_repository.update = mocker.Mock(return_value=office)

    result = service.update(office.office_id, office, Faker().uuid4())

    office_repository.update.assert_called_with(
        office_id=office.office_id, office=office)
    assert result == office


def test__update_office__return_None_when_id_not_exist(dependencies, mocker, office_factory):
    office_repository, parking_repository, seat_repository, service = dependencies.values()
    office = office_factory()
    office_repository.update = mocker.Mock(return_value=None)

    result = service.update(office.office_id, office, Faker().uuid4())

    office_repository.update.assert_called_with(
        office_id=office.office_id, office=office)
    assert result == None


def test__delete_office__was_called_correctly(dependencies, mocker, office_factory):
    office_repository, parking_repository, seat_repository, service = dependencies.values()
    office = office_factory()
    office_repository.get = mocker.Mock(return_value=office)
    office_repository.delete = mocker.Mock(return_value=True)

    result = service.delete(office.office_id, Faker().uuid4())

    office_repository.delete.assert_called_with(
        office_id=office.office_id)
    assert result


def test__delete_office__return_false_when_id_not_exist(dependencies, mocker, office_factory):
    office_repository, parking_repository, seat_repository, service = dependencies.values()
    office = office_factory()
    office_repository.get = mocker.Mock(return_value=office)
    office_repository.delete = mocker.Mock(return_value=False)

    result = service.delete(office.office_id, Faker().uuid4())

    office_repository.delete.assert_called_with(
        office_id=office.office_id)
    assert result == False


def test__get_office__was_called_correctly(dependencies, mocker, office_factory):
    office_repository, parking_repository, seat_repository, service = dependencies.values()
    office = office_factory()
    office_repository.get = mocker.Mock(return_value=office)
    service._populate_office = mocker.Mock(
        return_value=(office.seats, office.parkings))

    result = service.get(office.office_id)

    office_repository.get.assert_called_with(
        office_id=office.office_id)
    service._populate_office.assert_called_with(
        seats_ids=office.seats, parkings_ids=office.parkings)
    assert result == office


def test__get_office__return_None_when_id_not_exist(dependencies, mocker, office_factory):
    office_repository, parking_repository, seat_repository, service = dependencies.values()
    office = office_factory()
    office_repository.get = mocker.Mock(return_value=None)

    result = service.get(office.office_id)

    office_repository.get.assert_called_with(
        office_id=office.office_id)
    assert result == None


def test__find_office__was_called_correctly(dependencies, mocker, office_factory):
    office_repository, parking_repository, seat_repository, service = dependencies.values()
    office = office_factory()
    office2 = office_factory()
    criteria = mocker.Mock()
    office_repository.find = mocker.Mock(return_value=[office, office2])
    service._populate_office = mocker.Mock(return_value=([], []))

    result = service.find(criteria, populate=True)

    office_repository.find.assert_called_with(criteria=criteria)
    assert service._populate_office.call_count == 2
    assert result == [office, office2]


def test__find_office__return_empty_list_when_not_found(dependencies, mocker):
    office_repository, parking_repository, seat_repository, service = dependencies.values()
    criteria = mocker.Mock()
    office_repository.find = mocker.Mock(return_value=[])
    service._populate_office = mocker.Mock()

    result = service.find(criteria, populate=False)

    office_repository.find.assert_called_with(criteria=criteria)
    service._populate_office.assert_not_called()
    assert result == []


def test__populate_office__was_called_correctly(dependencies, mocker, office_factory):
    office_repository, parking_repository, seat_repository, service = dependencies.values()
    office = office_factory(parkings=['1', '2'], seats=['1', '2'])
    parking = mocker.Mock(parking_id='1')
    seat = mocker.Mock(seat_id='1')
    parking_repository.get = mocker.Mock(return_value=parking)
    seat_repository.get = mocker.Mock(return_value=seat)

    result = service._populate_office(office.seats, office.parkings)

    assert parking_repository.get.call_count == 2
    assert seat_repository.get.call_count == 2
    assert result == ([seat, seat], [parking, parking])


def test__populate_office__was_called_correctly(dependencies, mocker, office_factory):
    office_repository, parking_repository, seat_repository, service = dependencies.values()
    office = office_factory(parkings=['1', '2'], seats=['1', '2'])
    parking_repository.get = mocker.Mock(return_value=None)
    seat_repository.get = mocker.Mock(return_value=None)

    result = service._populate_office(office.seats, office.parkings)

    assert parking_repository.get.call_count == 2
    assert seat_repository.get.call_count == 2
    assert result == ([], [])
