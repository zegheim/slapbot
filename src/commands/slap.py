import logging
import random
from typing import List, Optional

import telegram
from src.config.tools import SLAP_TOOLS
from src.helpers.formatters import mention_user
from src.helpers.logging import add_logging
from src.helpers.types import User
from telegram import ChatAction, ParseMode


class SlapBot:
    def __init__(self, token: str, chat_id: int, parse_mode: str = ParseMode.HTML):
        """Responsible for crafting & sending messages.

        Parameters
        ----------
        token : str
            Telegram bot token.
        chat_id : int
            Numerical ID of the chat this bot will send messages to.
        parse_mode : str, optional
            How Telegram formats its message, by default ParseMode.HTML
            See https://core.telegram.org/bots/api#formatting-options for more information.
        """
        self.parse_mode = parse_mode
        self.chat_id = chat_id
        self.bot = telegram.Bot(token=token)

    @staticmethod
    def get_slap_tool() -> str:
        """Selects a random tool to slap someone with.

        Returns
        -------
        str
            Selected slapping tool.
        """

        return random.choice(SLAP_TOOLS)

    @staticmethod
    def craft_message(
        from_id: int, from_name: str, to_id: int, to_name: str, using: str
    ) -> str:
        """Crafts the slap message to be sent to Telegram.

        Parameters
        ----------
        from_id : int
            Numerical ID of the user initiating the slap action.
        from_name : str
            What to mention the initiator by.
        to_id : int
            Numerical ID of the user receiving the slap action.
        to_name : str
            What to mention the recipient by.
        using : str
            The tool to be used in this slap action.

        Returns
        -------
        str
            The crafted slap message.
        """
        sender = mention_user(from_id, from_name)
        recipient = mention_user(to_id, to_name)

        return f"{sender} slaps {recipient} with {using}!"

    @staticmethod
    @add_logging(level=logging.INFO)
    def get_name_from_user(user: User, logger: logging.Logger) -> str:
        """Attempts to get a valid name from the supplied user.

        Parameters
        ----------
        user : User
            User dictionary to parse a valid name from.

        Returns
        -------
        str
            Either first name, username, or user ID in order of precedence.
        """
        name = str(user["id"])

        if username := user.get("username"):
            name = username

        if first_name := user.get("first_name"):
            name = first_name

        logger.debug(f"Got {name} from {user}")

        return name

    @add_logging(level=logging.INFO)
    def slap(self, from_: User, to: User, logger: logging.Logger) -> None:
        """Test"""
        tool = SlapBot.get_slap_tool()
        logger.info("Will slap using {tool}.")

        from_name = SlapBot.get_name_from_user(from_)
        to_name = SlapBot.get_name_from_user(to)

        message = SlapBot.craft_message(from_["id"], from_name, to["id"], to_name, tool)

        self.bot.send_chat_action(chat_id=self.chat_id, action=ChatAction.TYPING)
        self.bot.send_message(
            chat_id=self.chat_id, text=message, parse_mode=self.parse_mode
        )


def slap(token: str, chat_id: int, sender: User, recipients: List[User]) -> None:
    bot = SlapBot(token, chat_id)

    if not recipients:
        bot.slap(sender, sender)
        return

    for recipient in recipients:
        bot.slap(sender, recipient)
