from http import HTTPStatus
from ...application import RideDeleter
from ....shared.domain.exceptions import PermissionsError
from ....shared.infrastructure.dependency_injection import ride_service_factory
from ....shared.infrastructure import ControllerResponse


def delete_ride_controller(event):
    ride_service = ride_service_factory()
    ride_deleter = RideDeleter(ride_service)
    try:
        result = ride_deleter.execute(
            user_id=event["user_id"], ride_id=event['ride_id'])
        status_code = HTTPStatus.OK if result else HTTPStatus.NOT_FOUND
        return ControllerResponse(
            status_code=status_code,
            body=None
        ).__dict__

    except PermissionsError as error:
        return ControllerResponse(
            status_code=HTTPStatus.FORBIDDEN,
            body={'message': error.args[0]}
        ).__dict__
