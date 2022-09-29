import json
import typing


class ControllerResponse:
    def __init__(self, status_code: int, body: typing.Union[dict, str]):
        self.status_code = status_code
        self.body = body

    def __str__(self):
        return str({
            "isBase64Encoded": False,
            'statusCode': self.status_code,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': self.body
        })

    def __eq__(self, other):
        return self.status_code == other.status_code
