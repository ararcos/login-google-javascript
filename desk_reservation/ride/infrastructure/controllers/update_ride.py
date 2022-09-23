from http import HTTPStatus
from pydantic import ValidationError
from ...domain import Ride
from ...application import RideUpdater
from ....shared.domain.exceptions import PermissionsError
from ....shared.infrastructure.dependency_injection import ride_service_factory
from ....shared.infrastructure import ControllerResponse, message_response


def update_ride_controller(event):

    try:
        ride_service = ride_service_factory()
        user_id = event.pop('user_id')
        ride_id = event['ride_id']
        ride = Ride(**event)
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
