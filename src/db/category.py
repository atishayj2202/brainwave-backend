from datetime import datetime
from typing import Type
from uuid import UUID

from src.db.base import Base, DBSchemaBase


class Category(DBSchemaBase):
    category_name: str
    parent_id: UUID | None = None
    is_deleted: datetime | None = None
    title: str | None = None
    description: str | None = None
    article_info: str | None = None
    remarks: str | None = None

    @classmethod
    def _schema_cls(cls) -> Type[Base]:
        return _Category


_Category = Base.from_schema_base(Category, "category")
