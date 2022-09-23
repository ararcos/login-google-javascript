from http import HTTPStatus
from pydantic import ValidationError
#pylint: disable=R0801

from ....shared.domain.exceptions.permissions_error import PermissionsError
from ....shared.infrastructure.controllers import message_response
from ....shared.infrastructure.controllers import ControllerResponse
from ....shared.infrastructure.dependency_injection import user_service_factory
from ...application.user_editor import UserEditor
from ...domain.entities.user import User


def edit_user_controller(event):
    try:
        user_service = user_service_factory()
        google_id = event['google_id']
        user = User(**event)
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
