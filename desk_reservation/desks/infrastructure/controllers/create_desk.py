from http import HTTPStatus
from pydantic import ValidationError
from ...application import DeskCreator
from ...domain.entities.desk import Desk
from ....shared.infrastructure.controllers import ControllerResponse
from ....shared.domain.exceptions.permissions_error import PermissionsError
from ....shared.infrastructure.controllers.message_response import message_response
from ....shared.infrastructure.dependency_injection.services_factory import desk_service_factory

# pylint:disable=duplicate-code
def create_desk_controller(event):
    try:
        desk_service = desk_service_factory()
        user_id = event.pop('user_id')
        desk = Desk(**event)
        desk_creator = DeskCreator(desk_service)

        result = desk_creator.execute(
            user_id=user_id,
            desk=desk
            ).__dict__
        print(result)
        return ControllerResponse(
            status_code=HTTPStatus.CREATED,
            body=result
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
