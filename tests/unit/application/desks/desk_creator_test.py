from faker import Faker

from desk_reservation.desks.application.desk_creator import DeskCreator

def test__return_desk_when_desk_is_created(mocker, desk_factory):
    desk = desk_factory()
    desk_service = mocker.Mock(
        create=mocker.Mock(return_value=desk)
    )

    desk_creator = DeskCreator(desk_service=desk_service)
    result = desk_creator.execute(desk=desk, user_id=Faker().uuid4())
    assert result is desk
