from typing import Type

from src.db.base import Base, DBSchemaBase


class WAMessage(DBSchemaBase):
    message_id: str
    message: str
    output_message: str
    wa_id: str

    @classmethod
    def _schema_cls(cls) -> Type[Base]:
        return _WAMessage


_WAMessage = Base.from_schema_base(WAMessage, "wa_history")
