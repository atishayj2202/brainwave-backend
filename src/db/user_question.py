from datetime import datetime
from typing import Type
from uuid import UUID

from src.db.base import Base, DBSchemaBase


class UserQuestion(DBSchemaBase):
    question_id: UUID
    user_id: UUID
    is_correct: bool | None = None

    @classmethod
    def _schema_cls(cls) -> Type[Base]:
        return _UserQuestion


_UserQuestion = Base.from_schema_base(UserQuestion, "user_questions")
