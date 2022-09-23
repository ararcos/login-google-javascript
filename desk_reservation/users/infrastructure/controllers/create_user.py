from http import HTTPStatus
from pydantic import ValidationError


from ....shared.domain.exceptions.permissions_error import PermissionsError
from ....shared.infrastructure.controllers import message_response
from ...domain.exceptions.incorrect_domain_error import IncorrectDomainError
from ....shared.infrastructure.controllers.controller_response import ControllerResponse
from ....shared.infrastructure.dependency_injection.services_factory import user_service_factory
from ...application.user_creator import UserCreator
from ...domain.entities.user import User


def create_user_controller(event):
    try:
        user_service = user_service_factory()
        google_id = event['google_id']
        user = User(**event)
        user_creator = UserCreator(user_service)
        result = user_creator.execute(google_id=google_id, user=user)
        return ControllerResponse(
            status_code=HTTPStatus.CREATED,
            body=result.__dict__
        ).__dict__

    except ValidationError:
        return ControllerResponse(
            status_code=HTTPStatus.BAD_REQUEST,
            body={"message": "Check User Attributes"}
        ).__dict__

    except PermissionsError as error:
        response = message_response(error.args)
        return ControllerResponse(status_code=HTTPStatus.FORBIDDEN,
            body=response).__dict__

    except IncorrectDomainError as error:
        response = message_response(error.args)
        return ControllerResponse(
            status_code=HTTPStatus.CONFLICT, body=response
        ).__dict__
