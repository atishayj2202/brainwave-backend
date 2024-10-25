from datetime import datetime
from typing import Type
from uuid import UUID

from src.db.base import Base, DBSchemaBase


class Game(DBSchemaBase):
    game_step: str = "1"
    user_id: UUID
    wait_status: str
    status: str
    is_deleted: datetime | None = None
    current_questions: list[UUID] = []
    completed_question: list[UUID] = []
    step_percentage: float = 0.0
    completed_at: datetime | None = None
    current_position: str = "1"

    @classmethod
    def _schema_cls(cls) -> Type[Base]:
        return _Game


_Game = Base.from_schema_base(Game, "game")
