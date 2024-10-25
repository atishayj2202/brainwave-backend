from datetime import datetime
from typing import Type
from uuid import UUID

from src.db.base import Base, DBSchemaBase


class Message(DBSchemaBase):
    message: str
    user_id: UUID
    role: str
    status: str
    category_id: UUID | None = None
    is_deleted: datetime | None = None

    @classmethod
    def _schema_cls(cls) -> Type[Base]:
        return _Message


_Message = Base.from_schema_base(Message, "message")
