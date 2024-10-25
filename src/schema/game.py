from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class QuestionResponse(BaseModel):
    question_id: UUID
    question: str
    option_a: str
    option_b: str
    option_d: str
    option_c: str


class AnswerRequest(BaseModel):
    question_id: UUID
    selected_option: str  # A | B | C | D


class AnswerResponse(BaseModel):
    question_id: UUID
    answer_id: UUID
    status: str
    correct_answer_code: str
    next_question: QuestionResponse


class ActiveGameResponse(BaseModel):
    game_id: UUID
    current_position: str
    status: str
    current_question_progress: float
    current_question: QuestionResponse
    points: float


class ArchiveGameResponse(BaseModel):
    game_id: UUID
    created_at: datetime
    status: str
    completed_at: datetime | None = None


class UpdateGameRequest(BaseModel):
    current_position: str
    wait_status: str
    point_update: int
