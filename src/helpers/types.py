from typing import List, Literal, TypedDict, Union

from src.helpers.enums import ChatType, EntityType


class _UserBase(TypedDict):
    id: int
    is_bot: bool


class User(_UserBase, total=False):
    first_name: str
    last_name: str
    username: str
    language_code: str


class Entity(TypedDict):
    length: int
    offset: int


class BotCommand(Entity):
    type: Literal[EntityType.BOT_COMMAND]


class TextMention(Entity):
    type: Literal[EntityType.TEXT_MENTION]
    user: User


AnyEntity = Union[BotCommand, TextMention]


class Chat(TypedDict):
    id: int


class GroupChat(Chat):
    type: Literal[ChatType.GROUP]
    title: str
    all_members_are_administrators: bool


class _PrivateChatBase(Chat):
    type: Literal[ChatType.PRIVATE]


class PrivateChat(_PrivateChatBase, total=False):
    first_name: str
    last_name: str
    username: str


AnyChat = Union[GroupChat, PrivateChat]


# "from" is a reserved keyword, using alternative syntax to define types
Message = TypedDict(
    "Message",
    {
        "entities": List[Union[BotCommand, TextMention]],
        "from": User,
        "message_id": int,
        "text": str,
        "date": int,
        "chat": Chat,
    },
)


class Body(TypedDict):
    message: Message
    update_id: int
