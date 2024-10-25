from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class UserCreateRequest(BaseModel):
    email: str
    name: str
    firebase_user_id: str


class UserResponse(BaseModel):
    id: UUID
    email: str
    name: str


class SubCategoryResponse(BaseModel):
    id: UUID | None
    name: str | None = None
    description: str | None = None


class CategoryInfoResponse(BaseModel):
    id: UUID | None
    name: str | None = None
    description: str | None = None
    parent_id: UUID | None = None
    aka: str | None = None
    new_description: str | None = None
    children: list[SubCategoryResponse] = []
