from http import HTTPStatus

from ...application.desk_getter import FinderById
from ....shared.infrastructure.controllers import ControllerResponse
from ....shared.infrastructure.dependency_injection.services_factory import desk_service_factory


# pylint:disable=duplicate-code
def get_desk_controller(event):
    desk_service = desk_service_factory()
    desk_getter = FinderById(desk_service)
    result = desk_getter.execute(desk_id=event["desk_id"])
    response = (HTTPStatus.OK, result.__dict__) if result else( HTTPStatus.NOT_FOUND, None)
    return ControllerResponse(
        status_code=response[0],
        body=response[1]
    ).__dict__
