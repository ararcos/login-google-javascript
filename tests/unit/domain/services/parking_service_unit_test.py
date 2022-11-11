from typing import List
import pytest
from faker import Faker

from desk_reservation.parkings.domain.entities.parking import Parking
from desk_reservation.parkings.domain.services.parking_service import ParkingService
from desk_reservation.shared.domain.exceptions.id_not_found_error import IdNotFoundError
from desk_reservation.shared.domain.exceptions.name_already_exists_error import NameAlreadyExistsError
from desk_reservation.shared.domain.exceptions.permissions_error import PermissionsError


@pytest.fixture(name='dependencies')
def _service_dependencies(mocker):
    parking_repository = mocker.Mock()
    user_repository = mocker.Mock()
    office_repository = mocker.Mock()
    parking_service = ParkingService(
        parking_repository=parking_repository, user_repository=user_repository, office_repository=office_repository
    )
    return {
        'parking_repository': parking_repository,
        'user_repository': user_repository,
        'office_repository': office_repository,
        'service': parking_service,
    }


def test__create_parking__was_called_correctly(dependencies, mocker, parking_factory):
    parking_repository, user_repository, office_repository, service = dependencies.values()
    user_id = Faker().uuid4()
    parking = parking_factory()

    service.has_permissions = mocker.Mock(return_value=True)
    service.is_parking_name_repeated_in_same_office = mocker.Mock(return_value=False)

    service.create_parking(parking=parking, user_id=user_id)

    parking_repository.create.assert_called_with(parking)


def test__create_parking__raises_Permissions_Error(dependencies, mocker, parking_factory):
    parking_repository, user_repository, office_repository, service = dependencies.values()
    user_id = Faker().uuid4()
    parking = parking_factory()
    
    service.has_permissions = mocker.Mock(return_value=False)

    with pytest.raises(PermissionsError):
        service.create_parking(parking=parking, user_id=user_id)


def test__create_parking__raises_NameAlreadyExistsError(dependencies, mocker, parking_factory):
    parking_repository, user_repository, office_repository, service = dependencies.values()
    user_id = Faker().uuid4()
    parking = parking_factory()
    
    service.has_permissions = mocker.Mock(return_value=True)
    service.is_parking_name_repeated_in_same_office = mocker.Mock(return_value=True)

    with pytest.raises(NameAlreadyExistsError):
        service.create_parking(parking=parking, user_id=user_id)



def test__delete_parking__was_called_correctly(dependencies, mocker, parking_factory):
    parking_repository, user_repository, office_repository, service = dependencies.values()
    user_id = Faker().uuid4()
    parking_id = Faker().uuid4()
    office_id = Faker().uuid4()
    parking = parking_factory(parking_id=parking_id)

    service.has_permissions = mocker.Mock(return_value=True)
    
    service.parking_repository.delete = mocker.Mock(return_value=True)
    result = service.delete_parking(parking_id=parking.parking_id, user_id=user_id, office_id=office_id)
    
    assert result == True


def test__delete_parking__raise_permissions_error(dependencies, mocker, parking_factory):
    parking_repository, user_repository, office_repository, service = dependencies.values()
    user_id = Faker().uuid4()
    parking_id = Faker().uuid4()
    office_id = Faker().uuid4()
    parking = parking_factory(parking_id=parking_id)

    service.has_permissions = mocker.Mock(return_value=False)

    with pytest.raises(PermissionsError):
        service.delete_parking(parking_id=parking.parking_id,
                            user_id=user_id, office_id=office_id)


def test__delete_parking__raise_id_not_found(dependencies, mocker, parking_factory):
    parking_repository, user_repository, office_repository, service = dependencies.values()
    user_id = Faker().uuid4()
    parking_id = Faker().uuid4()
    office_id = Faker().uuid4()
    parking = parking_factory(parking_id=parking_id)

    service.parking_repository.delete = mocker.Mock(return_value=False)
    service.has_permissions = mocker.Mock(return_value=True)

    with pytest.raises(IdNotFoundError):
        service.delete_parking(parking_id=parking.parking_id,
                            user_id=user_id, office_id=office_id)



def test__update_parking__was_called_correctly(dependencies, mocker, parking_factory):
    parking_repository, user_repository, office_repository, service = dependencies.values()
    user_id = Faker().uuid4()
    parking_id = Faker(). uuid4()
    parking = parking_factory(parking_id=parking_id)

    service.has_permissions = mocker.Mock(return_value=True)
    service.is_parking_name_repeated_in_same_office = mocker.Mock(return_value=False)
    parking_repository.update = mocker.Mock(return_value=parking)
    
    result = service.update_parking(user_id=user_id, parking=parking)

    assert result == parking

def test__update_parking__raise_permissions_error(dependencies, mocker, parking_factory):
    parking_repository, user_repository, office_repository, service = dependencies.values()
    user_id = Faker().uuid4()
    parking_id = Faker().uuid4()
    parking = parking_factory(parking_id=parking_id)

    service.has_permissions = mocker.Mock(return_value=False)
    parking_repository.update = mocker.Mock(return_value=parking)

    with pytest.raises(PermissionsError):
        service.update_parking(user_id=user_id, parking=parking)


def test__update_parking__raise_NameAlreadyExistsError(dependencies, mocker, parking_factory):
    parking_repository, user_repository, office_repository, service = dependencies.values()
    user_id = Faker().uuid4()
    parking_id = Faker().uuid4()
    parking = parking_factory(parking_id=parking_id)

    service.has_permissions = mocker.Mock(return_value=True)
    service.is_parking_name_repeated_in_same_office = mocker.Mock(return_value=True)
    parking_repository.update = mocker.Mock(return_value=parking)

    with pytest.raises(NameAlreadyExistsError):
        service.update_parking(user_id=user_id, parking=parking)


def test__update_parking__raise_id_not_found(dependencies, mocker, parking_factory):
    parking_repository, user_repository, office_repository, service = dependencies.values()
    user_id = Faker().uuid4()
    parking_id = Faker().uuid4()
    parking = parking_factory(parking_id=parking_id)

    service.has_permissions = mocker.Mock(return_value=True)
    service.is_parking_name_repeated_in_same_office = mocker.Mock(return_value=False)
    parking_repository.update = mocker.Mock(return_value=None)

    with pytest.raises(IdNotFoundError):
        service.update_parking(user_id=user_id, parking=parking)



def test__get_parking_by_id__return_parking_correctly(dependencies, mocker, parking_factory):
    parking_repository, user_repository, office_repository, service = dependencies.values()
    parking_id = Faker().uuid4()
    parking = parking_factory(parking_id=parking_id)

    parking_repository.get = mocker.Mock(return_value=parking)

    result = service.get_parking_by_id(parking_id)

    assert result == parking


def test__get_parking_by_id__raise_id_not_found_error(dependencies, mocker):
    parking_repository, user_repository, office_repository, service = dependencies.values()
    parking_id = Faker().uuid4()

    parking_repository.get = mocker.Mock(return_value=None)

    with pytest.raises(IdNotFoundError):
        service.get_parking_by_id(parking_id)


def test__find_parkings__was_called_correctly(dependencies, mocker):
    parking_repository, user_repository, office_repository, service = dependencies.values()
    criteria = mocker.Mock()

    service.find_parkings(criteria)

    parking_repository.find.was_called_with(criteria)


def test__user_is_admin__return_true(dependencies, mocker, parking_factory, user_factory):
    parking_repository, user_repository, office_repository, service = dependencies.values()
    user_id = Faker().uuid4()
    user = user_factory(google_id=user_id, admin=True)
    user_repository.get = mocker.Mock(return_value=user)

    result = service.user_is_admin(user_id)

    assert result == True


def test__user_is_admin__return_false_because_user_not_admin(dependencies, mocker, user_factory):
    parking_repository, user_repository, office_repository, service = dependencies.values()
    user_id = Faker().uuid4()
    user = user_factory(google_id=user_id, admin=False)
    user_repository.get = mocker.Mock(return_value=user)

    result = service.user_is_admin(user_id)

    assert result == False


def test__user_is_admin__return_false_because_user_not_found(dependencies, mocker):
    parking_repository, user_repository, office_repository, service = dependencies.values()
    user_id = Faker().uuid4()
    user_repository.get = mocker.Mock(return_value=None)

    result = service.user_is_admin(user_id)

    assert result == False


def test__user_is_manager__return_true(dependencies, mocker, office_factory):
    parking_repository, user_repository, office_repository, service = dependencies.values()
    user_id = Faker().uuid4()
    office_id = Faker().uuid4()
    office = office_factory()
    office.managers += [user_id]

    office_repository.get = mocker.Mock(return_value=office)

    result = service.user_is_manager(user_id=user_id, office_id=office_id)

    assert result == True


def test__user_is_manager__return_false_because_office_not_found(dependencies, mocker):
    parking_repository, user_repository, office_repository, service = dependencies.values()
    user_id = Faker().uuid4()
    office_id = Faker().uuid4()
    office_repository.get = mocker.Mock(return_value=None)

    result = service.user_is_manager(user_id=user_id, office_id=office_id)

    assert result == False


def test__user_is_manager__return_false_because_not_manager(dependencies, mocker, office_factory):
    parking_repository, user_repository, office_repository, service = dependencies.values()
    user_id = Faker().uuid4()
    office_id = Faker().uuid4()
    office = office_factory()

    office_repository.get = mocker.Mock(return_value=office)

    result = service.user_is_manager(user_id=user_id, office_id=office_id)

    assert result == False


def test__has_permissions__return_true_because_is_manager(dependencies, mocker):
    parking_repository, user_repository, office_repository, service = dependencies.values()
    user_id = Faker().uuid4()
    office_id = Faker().uuid4()

    service.user_is_manager = mocker.Mock(return_value=True)
    service.user_is_admin = mocker.Mock(return_value=False)

    result = service.has_permissions(
        user_id=user_id, office_id=office_id)

    assert result == True


def test__has_permissions__return_false_because_not_admin_or_manager(dependencies, mocker):
    parking_repository, user_repository, office_repository, service = dependencies.values()
    user_id = Faker().uuid4()
    office_id = Faker().uuid4()

    service.user_is_manager = mocker.Mock(return_value=False)
    service.user_is_admin = mocker.Mock(return_value=False)

    result = service.has_permissions(
        user_id=user_id, office_id=office_id)

    assert result == False


def test__is_parking_name_repeated_in_same_office__returns_false(dependencies, mocker):
    parking_repository, user_repository, office_repository, service = dependencies.values()
    name = Faker().name()
    office_id = Faker().uuid4()
    
    service.find_parkings = mocker.Mock(return_value=[])
    
    result = service.is_parking_name_repeated_in_same_office(name=name, office_id=office_id)
    
    assert result == False
    
def test__is_parking_name_repeated_in_same_office__returns_true(dependencies, mocker, parking_factory):
    parking_repository, user_repository, office_repository, service = dependencies.values()
    name = Faker().name()
    office_id = Faker().uuid4()
    parkings_found: List[Parking]= [parking_factory(name=name, ) for _ in range(3)]
    
    service.find_parkings = mocker.Mock(return_value=parkings_found)
    
    result = service.is_parking_name_repeated_in_same_office(name=name, office_id=office_id)
    assert_list = [True for parking in parkings_found if parking.name==name and parking.office_id==office_id]
    assert result == True
    assert all(assert_list) == True