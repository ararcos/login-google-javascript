from http import HTTPStatus
import json
from desk_reservation.ride.application import RideDeleter
from desk_reservation.shared.domain.exceptions import PermissionsError
from desk_reservation.shared.infrastructure.dependency_injection import ride_service_factory
from desk_reservation.shared.infrastructure import ControllerResponse


def delete_ride_controller(event, context=None, callback=None):
    body = json.loads(event["body"])
    ride_service = ride_service_factory()
    ride_deleter = RideDeleter(ride_service)
    try:
        result = ride_deleter.execute(
            user_id=body["user_id"], ride_id=body['ride_id'])
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
