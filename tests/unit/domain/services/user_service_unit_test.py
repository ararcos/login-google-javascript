import pytest
from faker import Faker
from desk_reservation.shared.domain.exceptions.id_not_found_error import IdNotFoundError
from desk_reservation.shared.domain.exceptions.permissions_error import PermissionsError
from desk_reservation.users.domain.exceptions.incorrect_domain_error import IncorrectDomainError

from desk_reservation.users.domain.services.user_service import UserService
from tests.unit._factories.user_factory import user_factory


@pytest.fixture(name='dependencies')
def _service_dependencies(mocker):
    user_repository = mocker.Mock()
    user_service = UserService(user_repository=user_repository)
    return {
        'user_repository': user_repository,
        'service': user_service,
    }


def test__get_user_was_called_correctly(dependencies, mocker, user_factory):
    user_repository, service = dependencies.values()
    user = user_factory()
    user_repository.get = mocker.Mock(return_value=user)

    result = service.get_user(google_id=Faker().uuid4())

    assert result == user


def test__find_user_was_called_correctly(dependencies, mocker):
    user_repository, service = dependencies.values()
    criteria = mocker.Mock()
    user_repository.find = mocker.Mock()

    service.find_user(criteria=criteria)
    user_repository.find.assert_called_with(criteria)


def test__create_user__was_called_correctly(dependencies, mocker, user_factory):
    user_repository, service = dependencies.values()
    service.is_admin = mocker.Mock(return_value=True)
    service.correct_domain = mocker.Mock(return_value=True)
    user = user_factory()

    service.create_user(user_id=Faker().uuid4(), user=user)
    user_repository.create.assert_called_with(user)


def test__raise_an_exception_when_not_having_permissions_to_create_user(dependencies, mocker, user_factory):
    user_repository, service = dependencies.values()
    google_id = Faker().uuid4()
    user = user_factory(admin=False)
    service.is_admin = mocker.Mock(return_value=False)
    with pytest.raises(PermissionsError):
        service.create_user(user_id=google_id, user=user)


def test__raise_an_exception_when_user_email_domain_is_incorrect(dependencies, user_factory, mocker):
    user_repository, service = dependencies.values()
    google_id = Faker().uuid4()
    user = user_factory(admin=True)
    service.correct_domain = mocker.Mock(return_value=False)
    with pytest.raises(IncorrectDomainError):
        service.create_user(user_id=google_id, user=user)


def test__edit_user_was_called_correctly(dependencies, mocker, user_factory):
    user_repository, service = dependencies.values()
    user_id = Faker().uuid4()
    user = user_factory(
        google_id=user_id,
        admin=True
    )
    user_repository.get = mocker.Mock(return_value=user)
    service.is_admin = mocker.Mock(return_value=True)
    user_repository.edit = mocker.Mock(return_value=user)

    service.edit_user(user_id=user_id, user=user)

    user_repository.edit.assert_called_with(user=user, google_id=user_id)


def test__raise_an_error_when_not_having_permission_to_edit_user(dependencies, mocker, user_factory):
    user_repository, service = dependencies.values()
    user_id = Faker().uuid4()
    user = user_factory(
        admin=False
    )
    service.get_user = mocker.Mock(return_value=user)
    service.is_admin = mocker.Mock(return_vale=False)

    with pytest.raises(PermissionsError):
        service.edit_user(user_id=user_id, user=user)


def test__delete_user_was_called_correctly(dependencies, mocker, user_factory):
    user_repository, service = dependencies.values()
    user_id = Faker().uuid4()
    service.is_admin = mocker.Mock(return_value=True)
    user_repository.delete = mocker.Mock(return_value=True)

    result = service.delete_user(google_id=user_id, user_id=user_id)
    assert result == True


def test__raise_an_error_when_not_having_permission_to_delete_user(dependencies, mocker):
    user_repository, service = dependencies.values()
    google_id = Faker().uuid4()
    user_id = Faker().uuid4()
    service.is_admin = mocker.Mock(return_value=False)

    with pytest.raises(PermissionsError):
        service.delete_user(google_id=google_id, user_id=user_id)


def test__return_true_when_is_admin(dependencies, mocker, user_factory):
    user_repository, service = dependencies.values()
    google_id = Faker().uuid4()
    user = user_factory(
        google_id=google_id,
        admin=True
    )
    user_repository.get = mocker.Mock(return_value=user)

    result = service.is_admin(google_id)

    assert result == True


def test__return_false_when_is_not_admin(dependencies, mocker, user_factory):
    user_repository, service = dependencies.values()
    google_id = Faker().uuid4()
    user = user_factory(
        google_id=google_id,
        admin=False
    )
    user_repository.get = mocker.Mock(return_value=user)

    result = service.is_admin(google_id)

    assert result == False


def test__return_true_when_is_correct_domain(dependencies, user_factory):
    user_repository, service = dependencies.values()
    user = user_factory(
        email='abc@ioet.com'
    )
    result = service.correct_domain(user)

    assert result == True


def test__return_false_when_domain_is_incorrect(dependencies, user_factory):
    user_repository, service = dependencies.values()
    user = user_factory(
        email='abc@gmail.com'
    )
    result = service.correct_domain(user)

    assert result == False
