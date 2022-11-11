from faker import Faker
from .....desk_reservation.desks.application.desk_getter import FinderById


def test__find_a_desk_when_id_no_exists(mocker):
    desk_id = Faker().uuid4()
    desk_service = mocker.Mock(
        find_one=mocker.Mock(return_value=None)
    )
    desk_finder = FinderById(desk_service=desk_service)

    result = desk_finder.execute(desk_id)
    assert result is None


def test__find_a_desk_when_id_exist(mocker, desk_factory):
    desk_id = Faker().uuid4()
    desk = desk_factory(desk_id=desk_id)
    desk_service = mocker.Mock(
        get_desk_by_id=mocker.Mock(return_value=desk)
    )

    desk_finder = FinderById(desk_service=desk_service)

    result = desk_finder.execute(desk_id=desk_id)
    assert result.desk_id == desk_id
    assert result == desk
