from operator import itemgetter

import pytest
from faker import Faker

from desk_reservation.desks.domain.services.desk_service import DeskService
from desk_reservation.shared.domain.exceptions.permissions_error import PermissionsError
from desk_reservation.shared.domain.exceptions.name_already_exists_error import (
    NameAlreadyExistsError,
)
from desk_reservation.desks.domain.exceptions.too_many_seats_error import (
    TooManySeatsError,
)


faker = Faker()


@pytest.fixture(name="dependencies")
def _service_dependencies(mocker):
    desk_repository = mocker.Mock()
    user_repository = mocker.Mock()
    office_repository = mocker.Mock()
    seat_repository = mocker.Mock()
    seat_service = DeskService(
        desk_repository=desk_repository,
        user_repository=user_repository,
        office_repository=office_repository,
        seat_repository=seat_repository,
    )
    return {
        "service": seat_service,
        "desk_repository": desk_repository,
        "user_repository": user_repository,
        "office_repository": office_repository,
        "seat_repository": seat_repository,
    }


def test__create_desk__was_called_correctly(dependencies, mocker, desk_factory):
    service = itemgetter("service")(dependencies)
    user_id = faker.uuid4()
    service.has_permissions = mocker.Mock(return_value=True)
    service.desk_seats_list_len_validator = mocker.Mock(return_value=True)
    service.names_desk_validator = mocker.Mock(return_value=True)
    desk = desk_factory()

    service.create(user_id, desk)

    service.desk_repository.create.assert_called_with(desk)


def test__create_booking__raise_permissions_exception(
    dependencies, mocker, desk_factory
):
    service = itemgetter("service")(dependencies)
    user_id = faker.uuid4()
    service.has_permissions = mocker.Mock(return_value=False)
    service.desk_seats_list_len_validator = mocker.Mock(return_value=True)
    service.names_desk_validator = mocker.Mock(return_value=True)
    desk = desk_factory()

    with pytest.raises(PermissionsError):
        service.create(user_id, desk)


def test__get_desk__was_called_correctly(dependencies, mocker, desk_factory):
    service, desk_repository = itemgetter("service", "desk_repository")(dependencies)
    desk = desk_factory()
    desk_repository.get = mocker.Mock(return_value=desk)
    result = service.get(desk.desk_id)

    assert result == desk
    assert result.seats_list == desk.seats_list
    desk_repository.get.assert_called_with(desk.desk_id)


def test__get_desk__return_none__when_id_not_exist(dependencies, mocker, desk_factory):
    service, desk_repository = itemgetter("service", "desk_repository")(dependencies)
    desk = desk_factory()
    desk_repository.get = mocker.Mock(return_value=None)
    service.populate_desk = mocker.Mock()

    result = service.get(desk.desk_id)

    assert result is None
    assert service.populate_desk.call_count == 0


def test__find_desk__was_called_correctly__but_seats_ids_not_found(
    dependencies, mocker, desk_factory
):
    service, desk_repository = itemgetter("service", "desk_repository")(dependencies)
    desk1 = desk_factory()
    desk2 = desk_factory()
    criteria = mocker.Mock()
    desk_repository.find = mocker.Mock(return_value=[desk1, desk2])

    result = service.find(criteria, populate=True)

    assert result == [desk1, desk2]


def test__find_desk__return_empty_list_when_not_found(dependencies, mocker):
    service, desk_repository = itemgetter("service", "desk_repository")(dependencies)
    criteria = mocker.Mock()
    desk_repository.find = mocker.Mock(return_value=[])
    service.populate_desk = mocker.Mock(return_value=[])
    result = service.find(criteria, populate=True)

    assert result == []
    assert service.populate_desk.call_count == 0


def test__update_desk__was_called_correctly(
    dependencies, mocker, desk_factory, user_factory, office_factory
):
    service, desk_repository, office_repository, user_repository = itemgetter(
        "service", "desk_repository", "office_repository", "user_repository"
    )(dependencies)
    user = user_factory(admin=True)
    desk = desk_factory()
    office = office_factory()
    service.get = mocker.Mock(return_value=desk)
    desk_repository.update = mocker.Mock(return_value=desk)
    office_repository.get = mocker.Mock(return_value=office)
    user_repository.get = mocker.Mock(return_value=user)

    result = service.update(user.google_id, desk)

    desk_repository.update.assert_called_with(user.google_id, desk)
    assert result == desk


def test__update_desk__return_none_when_id_not_exist(
    dependencies, mocker, desk_factory, office_factory, user_factory
):
    service, desk_repository, office_repository, user_repository = itemgetter(
        "service", "desk_repository", "office_repository", "user_repository"
    )(dependencies)
    user = user_factory(admin=True)
    desk = desk_factory()
    office = office_factory()
    service.get = mocker.Mock(return_value=desk)
    desk_repository.update = mocker.Mock(return_value=None)
    office_repository.get = mocker.Mock(return_value=office)
    user_repository.get = mocker.Mock(return_value=user)

    result = service.update(user.google_id, desk)

    desk_repository.update.assert_called_with(user.google_id, desk)
    assert result is None


def test__update_desk__raise_permissions_error(
    dependencies, mocker, desk_factory, office_factory, user_factory
):
    service, desk_repository, office_repository, user_repository = itemgetter(
        "service", "desk_repository", "office_repository", "user_repository"
    )(dependencies)
    user = user_factory(admin=False)
    desk = desk_factory()
    office = office_factory()
    service.get = mocker.Mock(return_value=desk)
    desk_repository.update = mocker.Mock(return_value=None)
    office_repository.get = mocker.Mock(return_value=office)
    user_repository.get = mocker.Mock(return_value=user)

    with pytest.raises(PermissionsError):
        service.update(user.google_id, desk)


def test__delete_desk__was_called_correctly(dependencies, mocker, desk_factory):
    service, desk_repository = itemgetter("service", "desk_repository")(dependencies)
    desk = desk_factory()
    user_id = Faker().uuid4()
    desk_repository.get = mocker.Mock(return_value=desk)
    desk_repository.delete = mocker.Mock(return_value=True)

    result = service.delete(desk, user_id)

    desk_repository.delete.assert_called_with(user_id=user_id, desk_id=desk.desk_id)
    assert result


def test__delete_desk__return_false_when_id_not_exist(
    dependencies, mocker, desk_factory
):
    service, desk_repository = itemgetter("service", "desk_repository")(dependencies)
    desk = desk_factory()
    user_id = Faker().uuid4()
    desk_repository.get = mocker.Mock(return_value=desk)
    desk_repository.delete = mocker.Mock(return_value=False)

    result = service.delete(desk, user_id)

    desk_repository.delete.assert_called_with(user_id=user_id, desk_id=desk.desk_id)
    assert result is False


def test__desk_seats_list_len_validator__was_called_correctly(
    dependencies, desk_factory
):
    service = itemgetter("service")(dependencies)
    fake_seat_list = [faker.uuid4() for i in range(0, 4)]
    desk = desk_factory(seats_list=fake_seat_list)

    result = service.desk_seats_list_len_validator(desk)

    assert result is True


def test__desk_seats_list_len_validator__raise_too_many_eats_exception(
    dependencies, desk_factory
):
    service = itemgetter("service")(dependencies)
    fake_seat_list = [faker.uuid4() for i in range(0, 13)]
    desk = desk_factory(seats_list=fake_seat_list)

    with pytest.raises(TooManySeatsError):
        service.desk_seats_list_len_validator(desk)


def test__names_desk_validator__was_called_correctly(
    dependencies, desk_factory, office_factory
):
    service = itemgetter("service")(dependencies)
    desk = desk_factory()
    office = office_factory()

    result = service.names_desk_validator(desk, office)

    assert result is True


def test__names_desk_validator__raise_name_already_exist(
    dependencies, desk_factory, office_factory
):
    service = itemgetter("service")(dependencies)
    desk = desk_factory()
    desks_list = [faker.pystr() for _ in range(3)]
    desks_list = [*desks_list, desk.desk_name]
    office = office_factory(desks=desks_list)

    with pytest.raises(NameAlreadyExistsError):
        service.names_desk_validator(desk, office)


def test__has_permissions__was_called_correctly(
    dependencies, mocker, office_factory, user_factory
):
    service, user_repository = itemgetter("service", "user_repository")(dependencies)
    user_id = faker.uuid4()
    user = user_factory(google_id=user_id, admin=False)
    user_repository.get = mocker.Mock(return_value=user)
    managers = [faker.uuid4() for _ in range(3)]
    managers = [*managers, user_id]
    office = office_factory(managers=managers)

    result = service.has_permissions(user_id, office)

    assert result is True
