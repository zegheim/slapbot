import logging
import os

from src.helpers.logging import add_logging
from src.helpers.types import AnyEntity


@add_logging(level=logging.DEBUG)
def parse_entity(text: str, entity_info: AnyEntity, logger: logging.Logger) -> str:
    """Extracts the entity substring from the given text, based on the provided entity information.

    Parameters
    ----------
    text : str
        The raw text to extract an entity from.
    entity_info : AnyEntity
        Entity metadata as provided by Telegram API.

    Returns
    -------
    str
        Extracted entity string (or empty string if the provided metadata is flawed).
    """
    length = entity_info["length"]
    offset = entity_info["offset"]
    entity = text[offset : offset + length]
    logger.debug(f"Parsed {entity} from {text} (length={length}, offset={offset}).")
    return entity


def is_command(command: str, ref_command: str) -> bool:
    """
    Checks whether the given command matches the reference command.
    Handles the case where the command is suffixed with the bot handle.

    Parameters
    ----------
    command : str
        Command to check.
    ref_command : str
        Reference command to compare to.

    Returns
    -------
    bool
        True if the command matches the reference command.
    """
    return command in (
        ref_command,
        f"{ref_command}@{os.environ['TELEGRAM_BOT_HANDLE']}",
    )
