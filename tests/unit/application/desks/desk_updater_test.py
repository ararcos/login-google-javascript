from faker import Faker

from desk_reservation.desks.application.desk_updater import DeskUpdater


def test__update_an_desk_when_desk_id_not_exist(mocker, desk_factory):
    desk_id = Faker().uuid4()
    user_id = Faker().uuid4()
    desk = desk_factory(desk_id=desk_id)
    desk_service = mocker.Mock(
        update=mocker.Mock(return_value=None)
    )
    desk_updater = DeskUpdater(desk_service=desk_service)

    result = desk_updater.execute(desk=desk, user_id=user_id)
    assert result is None
