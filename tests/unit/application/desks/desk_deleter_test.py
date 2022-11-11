from faker import Faker
from desk_reservation.desks.application.desk_deleter import DeskDeleter



def test__find_raise_an_exception_when_desk_cannot_be_deleted(mocker):
    desk_id = Faker().uuid4()
    user_id = Faker().uuid4()
    desk_service = mocker.Mock(
        delete=mocker.Mock(return_value=False)
    )
    desk_deleter = DeskDeleter(desk_service=desk_service)

    result = desk_deleter.execute(desk_id=desk_id, user_id=user_id)
    assert result is False


def test__return_true_when_desk_is_deleted(mocker):
    desk_id = Faker().uuid4()
    user_id = Faker().uuid4()
    desk_service = mocker.Mock(
        delete=mocker.Mock(return_value=True)
    )
    desk_deleter = DeskDeleter(desk_service=desk_service)

    result = desk_deleter.execute(desk_id=desk_id, user_id=user_id)
    assert result is True
