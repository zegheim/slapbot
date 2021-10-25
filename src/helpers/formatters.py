from telegram import ParseMode


def mention_user(user_id: int, name: str, parse_mode: str = ParseMode.HTML) -> str:
    """Generate string expected by Telegram to mention a user inline.

    Parameters
    ----------
    user_id : int
        Numerical ID of the user you want to mention.
    name : str
        What to mention said user with.

    Returns
    -------
    str
        String expected by Telegram to mention a user inline.

    Raises
    ------
    NotImplementedError
        Raised if the supplied parse_mode has no corresponding implementation.
    """
    if parse_mode == ParseMode.HTML:
        return f'<a href="tg://user?id={user_id}">{name}</a>'
    elif parse_mode in (ParseMode.MARKDOWN, ParseMode.MARKDOWN_V2):
        return f"[{name}](tg://user?id={user_id})"

    raise NotImplementedError(f"parse_mode={parse_mode} is not supported!")
