from uuid import UUID

from fastapi import APIRouter, Depends
from starlette import status
from starlette.responses import Response

from src.auth.user_auth import VerifiedUser, verify_user
from src.client.database import DBClient
from src.db.user import User
from src.schema.user import UserCreateRequest
from src.service.user import UserService
from src.utils.client import getDBClient

USER_PREFIX = "/user"
user_router = APIRouter(prefix=USER_PREFIX)

CREATE_USER = "/create-user/"
GET_USER = "/get-user/"
GET_BASE_CATEGORY = "/get-base-category/"
GET_CATEGORY = "/{category_id}/get-category/"


@user_router.post(CREATE_USER)
async def create_user(
    request: UserCreateRequest, db_client: DBClient = Depends(getDBClient)
):
    UserService.create_user(request, db_client)
    return Response(status_code=status.HTTP_200_OK)


@user_router.get(GET_USER)
async def get_user(
    verified_user: VerifiedUser = Depends(verify_user),
):
    return UserService.get_user(verified_user.requesting_user)


@user_router.get(GET_BASE_CATEGORY)
async def get_base_category(db_client: DBClient = Depends(getDBClient)):
    return UserService.get_category(db_client=db_client, category_id=None)


@user_router.get(GET_CATEGORY)
async def get_category(
    category_id: UUID | None = None,
    db_client: DBClient = Depends(getDBClient),
):
    return UserService.get_category(db_client=db_client, category_id=category_id)
