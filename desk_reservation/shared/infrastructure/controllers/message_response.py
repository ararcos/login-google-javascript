from typing import Tuple


def message_response(message: Tuple[str, str] = None) -> dict:
    response = {
        'message': message[0]
    }
    if len(message) == 2:
        response['details'] = message[1]

    return response
