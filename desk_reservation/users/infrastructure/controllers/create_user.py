from http import HTTPStatus
import json
from pydantic import ValidationError

from desk_reservation.users.domain.entities.user import User

from desk_reservation.shared.infrastructure.dependency_injection.services_factory import (
    user_service_factory
    )
from desk_reservation.shared.domain.exceptions.permissions_error import PermissionsError
from desk_reservation.shared.infrastructure.controllers import message_response
from desk_reservation.users.domain.exceptions.incorrect_domain_error import IncorrectDomainError
from desk_reservation.shared.infrastructure.controllers.controller_response import (
    ControllerResponse
    )
from desk_reservation.users.application.user_creator import UserCreator


# pylint: disable=W0613
def create_user_controller(event, context=None, callback=None):
    try:
        user_service = user_service_factory()
        body = json.loads(event["body"])
        user_id = body.pop('user_id')
        user = User(**body)
        user_creator = UserCreator(user_service)
        result = user_creator.execute(google_id=user_id, user=user)
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
        return ControllerResponse(
            status_code=HTTPStatus.FORBIDDEN,
            body=response
        ).__dict__

    except IncorrectDomainError as error:
        response = message_response(error.args)
        return ControllerResponse(
            status_code=HTTPStatus.CONFLICT,
            body=response
        ).__dict__
