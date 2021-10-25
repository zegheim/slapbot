import json
import logging
import os
from typing import Dict

from src.commands.slap import SlapBot
from src.helpers.adapters import EntityNameAndType
from src.helpers.logging import add_logging
from src.helpers.message import send_message
from src.helpers.parsers import is_command, parse_entity
from src.helpers.types import EntityType, Message


def authorize(event: Dict, context: Dict) -> Dict[str, bool]:
    """Lambda handler to check if the supplied token path parameter matches our bot token.

    Parameters
    ----------
    event : Dict
        Payload sent by API Gateway. Please refer to
        https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-lambda-authorizer.html#http-api-lambda-authorizer.payload-format
        for full reference. Please refer to provider.httpApi.authorizers.TokenAuthorizer.payloadVersion for the latest payload version used.
    context : Dict
        Context sent by API Gateway. Not used in this function.

    Returns
    -------
    Dict[str, bool]
        True if supplied token matches our bot token, False otherwise.
    """
    token: str = event.get("pathParameters", {}).get("token", "")

    return {"isAuthorized": token == os.environ["TELEGRAM_BOT_TOKEN"]}


@add_logging(level=logging.DEBUG)
def bot_command(event: Dict, context: Dict, logger: logging.Logger) -> Dict[str, int]:
    message: Message = json.loads(event["body"])["message"]
    logger.debug(f"Received message={message} from Telegram API.")

    raw_message = message["text"]
    entities = message["entities"]
    if entities[0]["type"] != EntityType.BOT_COMMAND:
        logger.warning(f"{raw_message} is not a bot command, nothing to see here.")
        return {"statusCode": 200}

    chat_id = message["chat"]["id"]
    token: str = event["pathParameters"]["token"]

    command = parse_entity(raw_message, entities[0])
    if is_command(command, "/slap"):
        sender = EntityNameAndType.from_user(message["from"])
        recipients = [
            EntityNameAndType.from_entity(entity, raw_message)
            for entity in entities
            if entity["type"] == EntityType.MENTION
            or entity["type"] == EntityType.TEXT_MENTION
        ]

        bot = SlapBot(token, chat_id)
        for recipient in recipients:
            bot.slap(sender, recipient)

        if not recipients:
            bot.slap(sender, sender)
    else:
        logger.warning(f"{command} is not a valid command.")
        send_message(token, chat_id, f"{command} is not a valid command.")

    return {"statusCode": 200}
