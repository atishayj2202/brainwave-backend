from datetime import datetime
from typing import Type
from uuid import UUID

from src.db.base import Base, DBSchemaBase


class Question(DBSchemaBase):
    question: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    correct_option: str
    difficulty_level: str
    is_deleted: datetime | None = None

    @classmethod
    def _schema_cls(cls) -> Type[Base]:
        return _Question


_Question = Base.from_schema_base(Question, "questions")
