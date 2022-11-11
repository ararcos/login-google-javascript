import json
import os


HEADERS = os.getenv("HEADERS", "Content-Type")
ORIGIN = os.getenv("ALLOWED_ORIGIN", "")
METHODS = os.getenv("METHODS", "")

# pylint: disable=W0613
def cors_handler(event, context=None, callback=None):
    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Headers": f"{HEADERS}",
            "Access-Control-Allow-Origin": f"{ORIGIN}",
            "Access-Control-Allow-Methods": f"OPTIONS,{METHODS}",
        },
        "body": json.dumps(""),
    }
