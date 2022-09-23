from http import HTTPStatus

from ....shared.domain.exceptions.domain_error import DomainError
from ....shared.domain.exceptions.permissions_error import PermissionsError
from ....shared.infrastructure.controllers import message_response
from ....shared.infrastructure.controllers import ControllerResponse
from ....shared.infrastructure.dependency_injection import user_service_factory
from ...application.user_deleter import UserDeleter


def delete_user_controller(event):
    user_service = user_service_factory()
    google_id = event['google_id']
    user_id = event['user_id']
    user_deleter = UserDeleter(user_service)
    try:
        result = user_deleter.execute(
            google_id=google_id, user_id=user_id
        )
        status_code = HTTPStatus.OK if result else HTTPStatus.NOT_FOUND
        return ControllerResponse(
            status_code=status_code,
            body=None).__dict__

    except PermissionsError as error:
        response = message_response(error.args)
        return ControllerResponse(status_code=HTTPStatus.FORBIDDEN,
            body=response
        ).__dict__

    except DomainError as error:
        response = message_response(
            error.args
        )
        return ControllerResponse(
            status_code=HTTPStatus.BAD_REQUEST,
            body=response).__dict__
