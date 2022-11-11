from http import HTTPStatus
import json
from pydantic import ValidationError
from desk_reservation.desks.application import DeskCreator
from desk_reservation.desks.domain.entities.desk import Desk
from desk_reservation.shared.infrastructure.controllers import ControllerResponse
from desk_reservation.shared.domain.exceptions.permissions_error import PermissionsError
from desk_reservation.shared.infrastructure.controllers.message_response import message_response
from desk_reservation.shared.infrastructure.dependency_injection.services_factory import (
    desk_service_factory
    )

# pylint: disable=W0613 duplicate-code
def create_desk_controller(event, context=None, callback=None):
    try:
        body= json.loads(event["body"])
        desk_service = desk_service_factory()
        user_id = body.pop('user_id')
        desk = Desk(**body)
        desk_creator = DeskCreator(desk_service)

        result = desk_creator.execute(
            user_id=user_id,
            desk=desk
            )
        return ControllerResponse(
            status_code=HTTPStatus.CREATED,
            body=result.__dict__
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
