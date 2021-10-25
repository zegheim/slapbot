from typing import List, Literal, TypedDict, Union

from src.helpers.enums import ChatType, EntityType


class _UserRequired(TypedDict):
    id: int
    is_bot: bool
    first_name: str


class User(_UserRequired, total=False):
    last_name: str
    username: str
    language_code: str


class Entity(TypedDict):
    length: int
    offset: int


class BotCommand(Entity):
    type: Literal[EntityType.BOT_COMMAND]


class Mention(Entity):
    type: Literal[EntityType.MENTION]


class TextMention(Entity):
    type: Literal[EntityType.TEXT_MENTION]
    user: User


AnyEntity = Union[BotCommand, Mention, TextMention]


class Chat(TypedDict):
    id: int


class GroupChat(Chat):
    type: Literal[ChatType.GROUP]
    title: str
    all_members_are_administrators: bool


class _PrivateChatRequired(Chat):
    type: Literal[ChatType.PRIVATE]
    first_name: str


class PrivateChat(_PrivateChatRequired, total=False):
    last_name: str
    username: str


AnyChat = Union[GroupChat, PrivateChat]


Message = TypedDict(
    "Message",
    {
        "entities": List[AnyEntity],
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
