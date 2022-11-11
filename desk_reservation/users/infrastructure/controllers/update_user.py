from http import HTTPStatus
import json
from pydantic import ValidationError

#pylint: disable=R0801

from desk_reservation.shared.infrastructure.dependency_injection.services_factory import (
    user_service_factory
    )
from desk_reservation.shared.domain.exceptions.permissions_error import PermissionsError
from desk_reservation.shared.infrastructure.controllers import message_response
from desk_reservation.shared.infrastructure.controllers import ControllerResponse
from desk_reservation.users.application.user_editor import UserEditor
from desk_reservation.users.domain.entities.user import User

# pylint: disable=W0613 W0703
def update_user_controller(event, context=None, callback=None):
    try:
        user_service = user_service_factory()
        body = json.loads(event["body"])
        google_id = body['google_id']
        user = User(**body)
        user_editor = UserEditor(user_service)
        result = user_editor.execute(google_id=google_id, user=user)
        response = (HTTPStatus.OK, result.__dict__) if result else(
            HTTPStatus.NOT_FOUND, None)
        return ControllerResponse(
            status_code=response[0],
            body=response[1]
        ).__dict__

    except (ValidationError, KeyError):
        return ControllerResponse(
            status_code=HTTPStatus.BAD_REQUEST,
            body={"message": "Check User Attributes"}
        ).__dict__

    except PermissionsError as error:
        response = message_response(error.args)
        return ControllerResponse(
            status_code=HTTPStatus.FORBIDDEN,
            body=response
        ).__dict__
