from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Optional, Union

from src.helpers.enums import EntityType
from src.helpers.parsers import parse_entity
from src.helpers.types import AnyEntity, Mention, TextMention, User
from telegram import MessageEntity as TelegramEntity
from telegram import User as TelegramUser


@dataclass
class EntityNameAndType:
    """Adapter class that acts as a bridge between User / AnyEntity and telegram.MessageEntity.

    Raises
    ------
    NotImplementedError
        Only supports entities of types Mention and TextMention.
    """

    name: str
    user: Optional[User]
    type: Union[Literal[EntityType.MENTION], Literal[EntityType.TEXT_MENTION]]

    def __len__(self):
        return len(self.name)

    @staticmethod
    def from_user(user: User) -> EntityNameAndType:
        """
        Convenience method to convert a User object to an EntityNameAndType object.

        Parameters
        ----------
        user : User
            The User object to be converted.

        Returns
        -------
        EntityNameAndType
            Converted User object.
        """
        return EntityNameAndType(
            name=user["first_name"], user=user, type=EntityType.TEXT_MENTION
        )

    @staticmethod
    def from_entity(entity: AnyEntity, raw_message: str) -> EntityNameAndType:
        """
        Convenience method to convert an AnyEntity object to an EntityNameAndType object.

        Parameters
        ----------
        entity : AnyEntity
            The AnyEntity object to be converted.
        raw_message : str
            Raw text message that contains the entity. Needed to convert entities of type Mention.

        Returns
        -------
        EntityNameAndType
            Converted AnyEntity object.

        Raises
        ------
        NotImplementedError
            Only supports entities of types Mention and TextMention.
        """
        if entity["type"] == EntityType.MENTION:
            return EntityNameAndType._from_mention(entity, raw_message)
        if entity["type"] == EntityType.TEXT_MENTION:
            return EntityNameAndType._from_text_mention(entity)

        raise NotImplementedError(f"EntityType={entity['type']} is not supported.")

    @staticmethod
    def _from_text_mention(entity: TextMention) -> EntityNameAndType:
        """Implementation of EntityNameAndType.from_mention for entities of type TextMention.

        Parameters
        ----------
        entity : TextMention
            The TextMention object to be converted.

        Returns
        -------
        EntityNameAndType
            Converted TextMention object.
        """
        user = entity["user"]
        return EntityNameAndType(
            name=user["first_name"], user=user, type=entity["type"]
        )

    @staticmethod
    def _from_mention(entity: Mention, raw_message: str) -> EntityNameAndType:
        """Implementation of EntityNameAndType.from_mention for entities of type Mention.

        Parameters
        ----------
        entity : Mention
            The Mention object to be converted.
        raw_message : str
            Raw text message that contains the entity.

        Returns
        -------
        EntityNameAndType
            Converted Mention object.
        """
        name = parse_entity(raw_message, entity)
        return EntityNameAndType(name=name, user=None, type=entity["type"])

    def to_telegram_entity(self, offset: int) -> TelegramEntity:
        """Convert itself to telegram's MessageEntity object.

        Parameters
        ----------
        offset : int
            Offset in UTF-16 code units to the start of the entity.

        Returns
        -------
        TelegramEntity
            The converted MessageEntity object.
        """
        user = TelegramUser(**self.user) if self.user else None
        return TelegramEntity(self.type, offset, len(self), user=user)
