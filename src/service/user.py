from uuid import UUID

from starlette import status
from starlette.exceptions import HTTPException

from src.client.database import DBClient
from src.db.category import Category
from src.db.user import User
from src.schema.user import (
    CategoryInfoResponse,
    SubCategoryResponse,
    UserCreateRequest,
    UserResponse,
)


class UserService:

    @classmethod
    def create_user(cls, request: UserCreateRequest, db_client: DBClient):
        db_client.query(
            User.add,
            items=[
                User(
                    email=request.email,
                    name=request.name,
                    firebase_user_id=request.firebase_user_id,
                )
            ],
        )

    @classmethod
    def get_user(cls, user: User) -> UserResponse:
        return UserResponse(
            id=user.id,
            email=user.email,
            name=user.name,
        )

    @classmethod
    def get_category(
        cls, db_client: DBClient, category_id: UUID | None = None
    ) -> CategoryInfoResponse:
        category = db_client.query(
            Category.get_id,
            id=category_id,
            error_not_exist=False,
        )
        name = ""
        description = ""
        new_description = ""
        aka = ""
        parent_id = None
        if category is not None:
            description = category.description
            name = category.category_name
            parent_id = category.parent_id
            aka = category.remarks
            new_description = category.article_info
        sub_categories: list[Category] = db_client.query(
            Category.get_by_field_multiple,
            field="parent_id",
            match_value=category_id,
            error_not_exist=False,
        )
        if category is None and sub_categories is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found",
            )
        if sub_categories is None:
            sub_categories = []
        return CategoryInfoResponse(
            id=category_id,
            name=name,
            description=description,
            parent_id=parent_id,
            aka=aka,
            new_description=new_description,
            children=[
                SubCategoryResponse(
                    id=sub_category.id,
                    name=sub_category.category_name,
                    description=sub_category.description,
                )
                for sub_category in sub_categories
            ],
        )
