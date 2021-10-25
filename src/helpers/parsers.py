import logging

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
