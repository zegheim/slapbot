from telegram import Bot, ChatAction


def send_message(token: str, chat_id: int, message: str) -> None:
    """Helper function to send a text message to the specified chat.

    Parameters
    ----------
    token : str
        Telegram bot token.
    chat_id : int
        Numerical ID of the chat this bot will send the specified message to.
    message : str
        Message to be sent.
    """
    bot = Bot(token=token)
    bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)
    bot.send_message(chat_id=chat_id, text=message)
