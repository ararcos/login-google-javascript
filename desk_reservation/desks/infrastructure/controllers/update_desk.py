from http import HTTPStatus
from pydantic import ValidationError
from ...domain.entities.desk import Desk
from ...application.desk_updater import DeskUpdater
from ....shared.infrastructure.controllers import ControllerResponse
from ....shared.domain.exceptions.permissions_error import PermissionsError
from ....shared.infrastructure.controllers.message_response import message_response
from ....shared.infrastructure.dependency_injection.services_factory import (
    desk_service_factory,
)

# pylint:disable=duplicate-code
def update_desk_controller(event):
    try:
        desk_service = desk_service_factory()
        user_id = event.pop('user_id')
        desk = Desk(**event)
        desk_updater = DeskUpdater(desk_service)
        result = desk_updater.execute(user_id, desk)
        response = (HTTPStatus.OK, result.__dict__) if result else( HTTPStatus.NOT_FOUND, None)
        return ControllerResponse(
            status_code=response[0],
            body=response[1]
        ).__dict__

    except (ValidationError, KeyError) :
        return ControllerResponse(
            status_code=HTTPStatus.BAD_REQUEST,
            body={"message": "Check Desk Attributes"}
        ).__dict__

    except PermissionsError as error:
        response = message_response(error.args)
        return ControllerResponse(
            status_code=HTTPStatus.FORBIDDEN,
            body=response
        ).__dict__
