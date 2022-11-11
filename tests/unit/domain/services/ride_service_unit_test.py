from datetime import date, datetime, timedelta
from operator import itemgetter
from faker import Faker
import pytest

from desk_reservation.ride.domain.services.ride_service import RideService
from desk_reservation.shared.domain.exceptions.bad_request import BadRequestError
from desk_reservation.shared.domain.exceptions.permissions_error import PermissionsError


@pytest.fixture(name="dependencies")
def _service_dependencies(mocker):
    ride_repository = mocker.Mock()
    user_repository = mocker.Mock()
    seat_service = RideService(
        ride_repository=ride_repository, user_repository=user_repository
    )
    return {
        "service": seat_service,
        "ride_repository": ride_repository,
        "user_repository": user_repository,
    }


def test__ride_is_old__was_called_correctly(dependencies, ride_factory):
    service = itemgetter("service")(dependencies)
    ride = ride_factory(ride_date=datetime.today())

    result = service.ride_is_old(ride)

    assert result is False


def test__ride_is_old__was_called_correctly_but_return_true(dependencies, ride_factory):
    service = itemgetter("service")(dependencies)
    ride = ride_factory(ride_date=datetime.today() - timedelta(days=10))
    result = service.ride_is_old(ride)

    assert result is True


def test_user_is_driver_of_ride_was_called_correctly(dependencies):
    service = itemgetter("service")(dependencies)
    user_id = Faker().uuid4()
    offerer_user_id = Faker().uuid4()

    result = service.user_is_driver_of_ride(user_id, offerer_user_id)

    assert result is False


def test_user_is_driver_of_ride_was_called_correctly_but_return_true(dependencies):
    service = itemgetter("service")(dependencies)
    user_id = Faker().uuid4()
    offerer_user_id = user_id

    result = service.user_is_driver_of_ride(user_id, offerer_user_id)

    assert result is True


def test__create_ride__was_called_correctly(dependencies, ride_factory):
    service = itemgetter("service")(dependencies)
    ride = ride_factory(ride_date=datetime.today())
    service.create(ride)
    service.ride_repository.create.assert_called_with(ride)


def test__create_ride__raise_bad_request_exception(dependencies, ride_factory):
    service = itemgetter("service")(dependencies)
    ride = ride_factory(ride_date=datetime.today() - timedelta(days=10))
    with pytest.raises(BadRequestError):
        service.create(ride)


def test__find_by_id__return_a_ride__when_id_was_found(
    dependencies, mocker, ride_factory
):
    service, ride_repository = itemgetter(
        "service", "ride_repository")(dependencies)
    ride_id = Faker().uuid4()
    ride = ride_factory(ride_id=ride_id)
    service.populate_booking_ride = mocker.Mock(return_value=ride)
    ride_repository.find_by_id = mocker.Mock(return_value=ride)

    result = service.find_by_id(ride_id)

    assert ride_repository.find_by_id.called_with(ride_id)
    assert result is ride


def test__find_by_id__return_a_none__when_id_was_not_found(dependencies, mocker):
    service, ride_repository = itemgetter(
        "service", "ride_repository")(dependencies)
    ride_id = Faker().uuid4()
    ride_repository.find_by_id = mocker.Mock(return_value=None)

    result = service.find_by_id(ride_id)

    assert ride_repository.find_by_id.called_with(ride_id)
    assert result is None


def test__find_all__return_data_when_was_called_correctly(
    dependencies, mocker, ride_factory
):
    service, ride_repository = itemgetter(
        "service", "ride_repository")(dependencies)
    ride1 = ride_factory()
    ride2 = ride_factory()
    expected_rides = [ride1.copy(update={"passengers": ["1","2"]}), ride2.copy(
        update={"passengers": ["1","2"]})]
    service.populate_booking_ride = mocker.Mock(return_value=["1", "2"])
    criteria = mocker.Mock()
    ride_repository.find_all = mocker.Mock(return_value=[ride1, ride2])

    result = service.find_all(criteria)

    assert result == expected_rides


def test__find_all__was_called_correctly_but_any_ride_was_found(dependencies, mocker):
    service, ride_repository = itemgetter(
        "service", "ride_repository")(dependencies)
    criteria = mocker.Mock()
    ride_repository.find_all = mocker.Mock(return_value=[])
    service.populate_booking_ride = mocker.Mock()

    result = service.find_all(criteria)

    assert result == []
    assert service.populate_booking_ride.call_count == 0


def test_delete_was_called_correctly(dependencies, mocker, ride_factory):
    service, ride_repository = itemgetter(
        "service", "ride_repository")(dependencies)
    user_id = Faker().uuid4()
    ride_id = Faker().uuid4()
    ride = ride_factory(ride_id=ride_id, offerer_user_id=user_id)
    ride_repository.find_by_id = mocker.Mock(return_value=ride)
    ride_repository.delete = mocker.Mock(return_value=True)

    result = service.delete(user_id, ride_id)

    assert result is True


def test_delete_was_called_correctly__but_raise_permissions_error(
    dependencies, mocker, ride_factory
):
    service, ride_repository = itemgetter(
        "service", "ride_repository")(dependencies)
    user_id = Faker().uuid4()
    ride_id = Faker().uuid4()
    ride = ride_factory(ride_id=ride_id)
    ride_repository.find_by_id = mocker.Mock(return_value=ride)
    ride_repository.delete = mocker.Mock(return_value=True)

    with pytest.raises(PermissionsError):
        service.delete(user_id, ride_id)


def test__booking_ride__was_called_correctly(
    dependencies, mocker, ride_factory, ride_booking_factory
):
    service, ride_repository = itemgetter(
        "service", "ride_repository")(dependencies)
    ride = ride_factory(passengers=["1", "2"], total_spots=4)
    ride_booking = ride_booking_factory()
    ride_repository.find_by_id = mocker.Mock(return_value=ride)
    ride_repository.booking_ride = mocker.Mock(return_value=ride_booking)

    result = service.booking_ride(ride_booking, ride)

    assert result is ride_booking


def test__booking_ride__was_called_correctly_but_return_a_bad_request_error(
    dependencies, mocker, ride_factory, ride_booking_factory
):
    service, ride_repository = itemgetter(
        "service", "ride_repository")(dependencies)
    ride = ride_factory(passengers=["1", "2"], total_spots=1)
    ride_booking = ride_booking_factory()
    ride_repository.find_by_id = mocker.Mock(return_value=ride)
    ride_repository.booking_ride = mocker.Mock(return_value=ride_booking)
    with pytest.raises(BadRequestError):
        service.booking_ride(ride_booking, ride)


def test___ride_service_return_user_info_when_exist_an_user(
    dependencies, user_factory, mocker
):
    service = itemgetter("service")(dependencies)
    user_repository = itemgetter("user_repository")(dependencies)
    user = user_factory()
    user_repository.get = mocker.Mock(return_value=user)

    result = service.populate_user_info(user.google_id)

    assert result == user


def test__ride_service_return_booking_ride_when_id_booking_ride_exist(
    dependencies, ride_booking_factory, mocker
):
    service = itemgetter("service")(dependencies)
    ride_repository = itemgetter("ride_repository")(dependencies)
    ride_booking = ride_booking_factory()
    ride_repository.find_by_id_booking_ride = mocker.Mock(
        return_value=ride_booking)

    result = service.populate_booking_ride([ride_booking.ride_booking_id])
    assert result == [ride_booking]


def test__ride_service_return_empty_list_when_id_booking_ride_not_exist(
    dependencies, ride_booking_factory, mocker
):
    service = itemgetter("service")(dependencies)
    ride_repository = itemgetter("ride_repository")(dependencies)
    ride_booking = ride_booking_factory()
    ride_repository.find_by_id_booking_ride = mocker.Mock(return_value=None)

    result = service.populate_booking_ride([ride_booking.ride_booking_id])
    assert result == []
