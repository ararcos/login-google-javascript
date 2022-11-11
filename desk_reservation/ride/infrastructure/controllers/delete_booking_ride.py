from http import HTTPStatus
import json
from desk_reservation.ride.application import RideBookingDeleter
from desk_reservation.shared.domain.exceptions import PermissionsError
from desk_reservation.shared.infrastructure.dependency_injection import ride_service_factory
from desk_reservation.shared.infrastructure import ControllerResponse


def delete_booking_ride_controller(event, context=None, callback=None):
    body = json.loads(event["body"])
    ride_service = ride_service_factory()
    ride_booking_deleter = RideBookingDeleter(ride_service)
    try:
        result = ride_booking_deleter.execute(
            ride_booking_ids=body["ride_booking_ids"], ride_id=body['ride_id'])
        status_code = HTTPStatus.OK if result else HTTPStatus.NOT_FOUND
        return ControllerResponse(
            status_code=status_code,
            body=result
        ).__dict__

    except PermissionsError as error:
        return ControllerResponse(
            status_code=HTTPStatus.FORBIDDEN,
            body={'message': error.args[0]}
        ).__dict__
