import logging
import random

from src.config.tools import SLAP_TOOLS
from src.helpers.adapters import EntityNameAndType
from src.helpers.logging import add_logging
from telegram import Bot, ChatAction


class SlapBot:
    """Responsible for crafting & sending messages."""

    VERB = "slaps"
    VERB_ALT = "goes nuts and slaps"

    def __init__(self, token: str, chat_id: int):
        """Initialises the bot.

        Parameters
        ----------
        token : str
            Telegram bot token.
        chat_id : int
            Numerical ID of the chat this bot will send messages to.
        """
        self.chat_id = chat_id
        self.bot = Bot(token=token)

    @staticmethod
    def _get_slap_tool() -> str:
        """Selects a random tool to slap someone with.

        Returns
        -------
        str
            Selected slapping tool.
        """

        return random.choice(SLAP_TOOLS)

    @classmethod
    def _craft_message(
        cls, sender_name: str, recipient_name: str, using: str, is_slap_self: bool
    ) -> str:
        """Crafts the slap message to be sent to Telegram.

        Parameters
        ----------
        sender_name : str
            What to mention the sender by.
        recipient_name : str
            What to mention the recipient by.
        using : str
            The tool to be used in this slap action.
        is_slap_self : bool
            Whether to use an alternative verb meant for slapping oneself.
        Returns
        -------
        str
            The crafted slap message.
        """
        verb = cls.VERB if not is_slap_self else cls.VERB_ALT
        return f"{sender_name} {verb} {recipient_name} with {using}!"

    @classmethod
    def _get_recipient_offset(
        cls, sender: EntityNameAndType, is_slap_self: bool
    ) -> int:
        """
        Calculates the offset for the recipient in the crafted message.
        Assumes crafted message follows the <SENDER> <VERB> <RECIPIENT> format.

        Parameters
        ----------
        sender : EntityNameAndType
            Sender object.
        is_slap_self : bool
            Whether to use an alternative verb meant for slapping oneself when calculating offset.
        Returns
        -------
        int
            Offset for recipient in the crafted message.
        """
        verb = cls.VERB if not is_slap_self else cls.VERB_ALT
        return len(sender) + len(verb) + 2

    @add_logging(level=logging.DEBUG)
    def slap(
        self,
        sender: EntityNameAndType,
        recipient: EntityNameAndType,
        logger: logging.Logger,
        is_slap_self: bool = False,
    ) -> None:
        """Slaps the recipient on behalf of the sender.

        Parameters
        ----------
        sender : EntityNameAndType
            Sender object.
        recipient : EntityNameAndType
            Recipient object.
        is_slap_self : bool
            Whether to use an alternative verb meant for slapping oneself, by default False.
        """
        tool = SlapBot._get_slap_tool()
        logger.debug(f"sender={sender}, recipient={recipient}, tool={tool}")

        message = SlapBot._craft_message(
            sender.name, recipient.name, tool, is_slap_self
        )
        entities = [
            sender.to_telegram_entity(offset=0),
            recipient.to_telegram_entity(
                SlapBot._get_recipient_offset(sender, is_slap_self)
            ),
        ]
        self.bot.send_chat_action(chat_id=self.chat_id, action=ChatAction.TYPING)
        self.bot.send_message(chat_id=self.chat_id, text=message, entities=entities)
