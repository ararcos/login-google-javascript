from http import HTTPStatus
import asyncio
import logging

from desk_reservation.notifications.application import DriverAndRiderReminder
from desk_reservation.shared.infrastructure.dependency_injection.services_factory import (
    ride_service_factory, user_service_factory, slack_service_factory
)
from desk_reservation.shared.infrastructure import ControllerResponse, message_response

logger = logging.getLogger()
logger.setLevel(logging.INFO)
async def send_ride_reminder_controller(event, context=None):
    user_service = user_service_factory()
    ride_service = ride_service_factory()
    slack_service = slack_service_factory()

    try:
        driver_reminder = DriverAndRiderReminder(
            ride_service=ride_service,
            user_service=user_service,
            slack_message_service=slack_service)
        await driver_reminder.execute()
        logger.info('Ride reminder sent')
        return ControllerResponse(
            status_code=HTTPStatus.OK,
            body='driver reminder successfully sent').__dict__

    except Exception as error:
        logger.error(error)
        raise error


def handler(event, context):
    return asyncio.run(send_ride_reminder_controller(event, context))
