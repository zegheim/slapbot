import json
from typing import Any


def lambda_handler(event: dict, context: dict) -> dict[str, Any]:
    return {"statusCode": 200, "body": json.dumps("Hello from Lambda!")}
