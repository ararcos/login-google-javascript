

from desk_reservation.desks.application.desk_finder import DeskFinder


def test__find_desk_when_data_exists(mocker, desk_factory):
    desks = [desk_factory() for _ in range(3)]
    criteria = mocker.Mock()
    desk_service = mocker.Mock(
        find=mocker.Mock(return_value=desks)
    )

    desk_finder = DeskFinder(desk_service=desk_service)

    result = desk_finder.execute(criteria=criteria, populate=False)
    assert result == desks


def test__find_desk_when_data_no_exist(mocker):
    criteria = mocker.Mock()
    desk_service = mocker.Mock(
        find=mocker.Mock(return_value=[])
    )

    desk_finder = DeskFinder(desk_service=desk_service)

    result = desk_finder.execute(criteria=criteria, populate=False)
    assert result == []
