
from http import HTTPStatus

from desk_reservation.shared.domain.exceptions.id_not_found_error import IdNotFoundError


from ...application import DeskDeleter
from ....shared.domain.exceptions import PermissionsError
from ....shared.infrastructure import ControllerResponse
from ....shared.infrastructure.dependency_injection.services_factory import desk_service_factory

# pylint: disable=R0801
def delete_desk_controller(event):
    desk_service = desk_service_factory()
    desk_deleter = DeskDeleter(desk_service)

    try:
        result = desk_deleter.execute(
            desk_id=event['desk_id'], user_id=event['user_id'])
        status_code = HTTPStatus.OK if result else HTTPStatus.NOT_FOUND
        return ControllerResponse(
            status_code=status_code,
            body=None
        ).__dict__

    except IdNotFoundError as error:
        return ControllerResponse(
            status_code=HTTPStatus.BAD_REQUEST,
            body={'message': error.args[0]}
        ).__dict__

    except PermissionsError as error:
        return ControllerResponse(
            status_code=HTTPStatus.FORBIDDEN,
            body={'message': error.args[0]}
        ).__dict__
