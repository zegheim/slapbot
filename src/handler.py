import json
import os
from typing import Dict, Union


def authorize(event: Dict, context: Dict) -> Dict[str, bool]:
    token = event.get("pathParameters", {}).get("token")

    return {"isAuthorized": token == os.environ["TELEGRAM_BOT_TOKEN"]}


def slap(event: Dict, context: Dict) -> Dict[str, Union[str, int]]:
    body = {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "input": event,
    }

    return {"statusCode": 200, "body": json.dumps(body)}
