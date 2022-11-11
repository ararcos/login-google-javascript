import pytest
from faker import Faker

from desk_reservation.seats.domain.services.seat_service import SeatService
from desk_reservation.shared.domain.exceptions.id_not_found_error import IdNotFoundError
from desk_reservation.shared.domain.exceptions.name_already_exists_error import NameAlreadyExistsError
from desk_reservation.shared.domain.exceptions.permissions_error import PermissionsError


@pytest.fixture(name='dependencies')
def _service_dependencies(mocker):
    seat_repository = mocker.Mock()
    user_repository = mocker.Mock()
    office_repository = mocker.Mock()
    seat_service = SeatService(
        seat_repository=seat_repository, user_repository=user_repository, office_repository=office_repository
    )
    return {
        'seat_repository': seat_repository,
        'user_repository': user_repository,
        'office_repository': office_repository,
        'service': seat_service,
    }


def test__create_seat__was_called_correctly(dependencies, mocker, seat_factory):
    seat_repository, user_repository, office_repository, service = dependencies.values()
    user_id = Faker().uuid4()
    seat = seat_factory()

    service.user_is_admin_or_manager = mocker.Mock(return_value=True)
    service.is_seat_name_repeated_in_same_office = mocker.Mock(return_value=False)

    service.create_seat(seat=seat, user_id=user_id)

    seat_repository.create.assert_called_with(seat)


def test__create_seat__raises_Permissions_Error(dependencies, mocker, seat_factory):
    seat_repository, user_repository, office_repository, service = dependencies.values()
    user_id = Faker().uuid4()
    seat = seat_factory()

    service.user_is_admin_or_manager = mocker.Mock(return_value=False)

    with pytest.raises(PermissionsError):
        service.create_seat(seat=seat, user_id=user_id)


def test__create_seat__raises_NameAlreadyExistsError(dependencies, mocker, seat_factory):
    seat_repository, user_repository, office_repository, service = dependencies.values()
    user_id = Faker().uuid4()
    seat = seat_factory()
    
    service.user_is_admin_or_manager = mocker.Mock(return_value=True)
    service.is_seat_name_repeated_in_same_office = mocker.Mock(return_value=True)

    with pytest.raises(NameAlreadyExistsError):
        service.create_seat(seat=seat, user_id=user_id)



def test__delete_seat__was_called_correctly(dependencies, mocker, seat_factory):
    seat_repository, user_repository, office_repository, service = dependencies.values()
    user_id = Faker().uuid4()
    office_id = Faker().uuid4()
    seat_id = Faker().uuid4()
    seat = seat_factory(seat_id=seat_id)

    service.user_is_admin_or_manager = mocker.Mock(return_value=True)
    service.is_seat_name_repeated_in_same_office = mocker.Mock(return_value=False)
    
    service.seat_repository.delete = mocker.Mock(return_value=True)
    result = service.delete_seat(seat_id=seat.seat_id,
                        user_id=user_id, office_id=office_id)
    
    assert result == True


def test__delete_seat__raise_permissions_error(dependencies, mocker, seat_factory):
    seat_repository, user_repository, office_repository, service = dependencies.values()
    user_id = Faker().uuid4()
    office_id = Faker().uuid4()
    seat_id = Faker().uuid4()
    seat = seat_factory(seat_id=seat_id)

    service.user_is_admin_or_manager = mocker.Mock(return_value=False)

    with pytest.raises(PermissionsError):
        service.delete_seat(seat_id=seat.seat_id,
                            user_id=user_id, office_id=office_id)


def test__delete_seat__raise_id_not_found(dependencies, mocker, seat_factory):
    seat_repository, user_repository, office_repository, service = dependencies.values()
    user_id = Faker().uuid4()
    office_id = Faker().uuid4()
    seat_id = Faker().uuid4()
    seat = seat_factory(seat_id=seat_id)

    service.seat_repository.delete = mocker.Mock(return_value=False)
    service.user_is_admin_or_manager = mocker.Mock(return_value=True)

    with pytest.raises(IdNotFoundError):
        service.delete_seat(seat_id=seat.seat_id,
                            user_id=user_id, office_id=office_id)


def test__delete_many__return_list_of_seats_when_were_deleted(mocker, dependencies):
    seat_repository, user_repository, office_repository, service = dependencies.values()
    seats = [Faker().uuid4()]
    
    seat_repository.delete = mocker.Mock(return_value=True)
    
    result = service.delete_many_seats(seats)
    
    assert result == seats
    

def test__delete_many__return_empty_list_of_seats_when_none_was_deleted(mocker, dependencies):
    seat_repository, user_repository, office_repository, service = dependencies.values()
    seats = [Faker().uuid4()]
    
    seat_repository.delete = mocker.Mock(return_value=False)
    
    result = service.delete_many_seats(seats)
    
    assert result == []


def test__update_seat__was_called_correctly(dependencies, mocker, seat_factory):
    seat_repository, user_repository, office_repository, service = dependencies.values()
    user_id = Faker().uuid4()
    seat_id = Faker(). uuid4()
    seat = seat_factory(seat_id=seat_id)

    service.user_is_admin_or_manager = mocker.Mock(return_value=True)
    service.is_seat_name_repeated_in_same_office = mocker.Mock(return_value=False)
    seat_repository.update = mocker.Mock(return_value=seat)
    
    result = service.update_seat(user_id=user_id, seat=seat)

    assert result == seat

def test__update_seat__raise_permissions_error(dependencies, mocker, seat_factory):
    seat_repository, user_repository, office_repository, service = dependencies.values()
    user_id = Faker().uuid4()
    seat_id = Faker().uuid4()
    seat = seat_factory(seat_id=seat_id)

    service.user_is_admin_or_manager = mocker.Mock(return_value=False)
    seat_repository.update = mocker.Mock(return_value=seat)

    with pytest.raises(PermissionsError):
        service.update_seat(user_id=user_id, seat=seat)


def test__update_seat__raise_NameAlreadyExistsError(dependencies, mocker, seat_factory):
    seat_repository, user_repository, office_repository, service = dependencies.values()
    user_id = Faker().uuid4()
    seat_id = Faker().uuid4()
    seat = seat_factory(seat_id=seat_id)

    service.user_is_admin_or_manager = mocker.Mock(return_value=True)
    service.is_seat_name_repeated_in_same_office = mocker.Mock(return_value=True)
    seat_repository.update = mocker.Mock(return_value=seat)

    with pytest.raises(NameAlreadyExistsError):
        service.update_seat(user_id=user_id, seat=seat)



def test__update_seat__raise_id_not_found(dependencies, mocker, seat_factory):
    seat_repository, user_repository, office_repository, service = dependencies.values()
    user_id = Faker().uuid4()
    seat_id = Faker().uuid4()
    seat = seat_factory(seat_id=seat_id)

    service.user_is_admin_or_manager = mocker.Mock(return_value=True)
    service.is_seat_name_repeated_in_same_office = mocker.Mock(return_value=False)
    
    seat_repository.update = mocker.Mock(return_value=None)

    with pytest.raises(IdNotFoundError):
        service.update_seat(user_id=user_id, seat=seat)



def test__get_seat_by_id__return_seat_correctly(dependencies, mocker, seat_factory):
    seat_repository, user_repository, office_repository, service = dependencies.values()
    seat_id = Faker().uuid4()
    seat = seat_factory(seat_id=seat_id)

    seat_repository.get = mocker.Mock(return_value=seat)

    result = service.get_seat_by_id(seat_id)

    assert result == seat


def test__get_seat_by_id__raise_id_not_found_error(dependencies, mocker):
    seat_repository, user_repository, office_repository, service = dependencies.values()
    seat_id = Faker().uuid4()

    seat_repository.get = mocker.Mock(return_value=None)

    with pytest.raises(IdNotFoundError):
        service.get_seat_by_id(seat_id)


def test__find_seats__was_called_correctly(dependencies, mocker):
    seat_repository, user_repository, office_repository, service = dependencies.values()
    criteria = mocker.Mock()

    service.find_seats(criteria)

    seat_repository.find.was_called_with(criteria)


def test__user_is_admin__return_true(dependencies, mocker, seat_factory, user_factory):
    seat_repository, user_repository, office_repository, service = dependencies.values()
    user_id = Faker().uuid4()
    user = user_factory(google_id=user_id, admin=True)
    user_repository.get = mocker.Mock(return_value=user)

    result = service.user_is_admin(user_id)

    assert result == True


def test__user_is_admin__return_false_because_user_not_admin(dependencies, mocker, user_factory):
    seat_repository, user_repository, office_repository, service = dependencies.values()
    user_id = Faker().uuid4()
    user = user_factory(google_id=user_id, admin=False)
    user_repository.get = mocker.Mock(return_value=user)

    result = service.user_is_admin(user_id)

    assert result == False


def test__user_is_admin__return_false_because_user_not_found(dependencies, mocker):
    seat_repository, user_repository, office_repository, service = dependencies.values()
    user_id = Faker().uuid4()
    user_repository.get = mocker.Mock(return_value=None)

    result = service.user_is_admin(user_id)

    assert result == False


def test__user_is_manager__return_true(dependencies, mocker, office_factory):
    seat_repository, user_repository, office_repository, service = dependencies.values()
    user_id = Faker().uuid4()
    office_id = Faker().uuid4()
    office = office_factory(office_id=office_id)
    office.managers += [user_id]

    office_repository.get = mocker.Mock(return_value=office)

    result = service.user_is_manager(user_id=user_id, office_id=office_id)

    assert result == True


def test__user_is_manager__return_false_because_office_not_found(dependencies, mocker):
    seat_repository, user_repository, office_repository, service = dependencies.values()
    user_id = Faker().uuid4()
    office_id = Faker().uuid4()

    office_repository.get = mocker.Mock(return_value=None)

    result = service.user_is_manager(user_id=user_id, office_id=office_id)

    assert result == False


def test__user_is_manager__return_false_because_not_manager(dependencies, mocker, office_factory):
    seat_repository, user_repository, office_repository, service = dependencies.values()
    user_id = Faker().uuid4()
    office_id = Faker().uuid4()
    office = office_factory()

    office_repository.get = mocker.Mock(return_value=office)

    result = service.user_is_manager(user_id=user_id, office_id=office_id)

    assert result == False


def test__user_is_admin_or_manager__return_true_because_is_manager(dependencies, mocker):
    seat_repository, user_repository, office_repository, service = dependencies.values()
    user_id = Faker().uuid4()
    office_id = Faker().uuid4()

    service.user_is_manager = mocker.Mock(return_value=True)
    service.user_is_admin = mocker.Mock(return_value=False)

    result = service.user_is_admin_or_manager(
        user_id=user_id, office_id=office_id)

    assert result == True


def test__user_is_admin_or_manager__return_false_because_not_admin_or_manager(dependencies, mocker):
    seat_repository, user_repository, office_repository, service = dependencies.values()
    user_id = Faker().uuid4()
    office_id = Faker().uuid4()

    service.user_is_manager = mocker.Mock(return_value=False)
    service.user_is_admin = mocker.Mock(return_value=False)

    result = service.user_is_admin_or_manager(
        user_id=user_id, office_id=office_id)

    assert result == False
