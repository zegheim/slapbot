from enum import Enum


class StrEnum(str, Enum):
    """With str mix-in to allow for string comparison.

    Example
    -------

    class MyEnum(StrEnum):
        FOO = "foo"

    >>> assert MyEnum.FOO == "foo"
    """

    pass


class EntityType(StrEnum):
    BOT_COMMAND = "bot_command"
    TEXT_MENTION = "text_mention"


class ChatType(StrEnum):
    PRIVATE = "private"
    GROUP = "group"
