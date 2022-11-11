from http import HTTPStatus
import json
from pydantic import ValidationError
from desk_reservation.ride.domain import Ride
from desk_reservation.ride.application import RideUpdater
from desk_reservation.shared.domain.exceptions import PermissionsError
from desk_reservation.shared.infrastructure.dependency_injection import ride_service_factory
from desk_reservation.shared.infrastructure import ControllerResponse, message_response


def update_ride_controller(event, context=None, callback=None):

    try:
        ride_service = ride_service_factory()
        body = json.loads(event["body"])
        user_id = body.pop('user_id')
        ride_id = body['ride_id']
        ride = Ride(**body)
        ride_updater = RideUpdater(ride_service)
        result = ride_updater.execute(
            user_id=user_id,
            ride_id=ride_id,
            edited_ride=ride
        )
        response = (HTTPStatus.OK, result.__dict__) if result else(HTTPStatus.NOT_FOUND, None)

        return ControllerResponse(
            status_code=response[0],
            body=response[1]
        ).__dict__

    except (ValidationError, KeyError) :
        return ControllerResponse(
            status_code=HTTPStatus.BAD_REQUEST,
            body={"message": "Check Ride Attributes"}
        ).__dict__

    except PermissionsError as error:
        return ControllerResponse(
            status_code=HTTPStatus.FORBIDDEN,
            body=message_response(error.args)
        ).__dict__
