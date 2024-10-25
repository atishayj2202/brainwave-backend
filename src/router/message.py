from uuid import UUID

from fastapi import APIRouter, Depends

from src.auth.user_auth import VerifiedUser, verify_user
from src.client.database import DBClient
from src.schema.message import MessageRequest, MessageResponse
from src.service.message import MessageService
from src.utils.client import getDBClient

MESSAGE_PREFIX = "/message"
message_router = APIRouter(prefix=MESSAGE_PREFIX)

GET_MESSAGES = "/get-messages/"
GET_AI_REPLY = "/get-ai-reply/"
GET_CATEGORY_MESSAGES = "/{category_id}/get-messages/"
GET_CATEGORY_AI_REPLY = "/{category_id}/get-ai-reply/"


@message_router.get(GET_MESSAGES, response_model=list[MessageResponse])
async def get_messages(
    verified_user: VerifiedUser = Depends(verify_user),
    db_client: DBClient = Depends(getDBClient),
):
    return MessageService.get_all_messages(
        user=verified_user.requesting_user, db_client=db_client
    )


@message_router.post(GET_AI_REPLY, response_model=MessageResponse)
async def get_ai_reply(
    request: MessageRequest,
    verified_user: VerifiedUser = Depends(verify_user),
    db_client: DBClient = Depends(getDBClient),
):
    return MessageService.get_ai_reply(
        request=request,
        user=verified_user.requesting_user,
        db_client=db_client,
        rag=False,
    )


@message_router.get(GET_CATEGORY_MESSAGES, response_model=list[MessageResponse])
async def get_messages(
    category_id: UUID,
    verified_user: VerifiedUser = Depends(verify_user),
    db_client: DBClient = Depends(getDBClient),
):
    return MessageService.get_all_messages(
        user=verified_user.requesting_user, db_client=db_client, category_id=category_id
    )


@message_router.post(GET_CATEGORY_AI_REPLY, response_model=MessageResponse)
async def get_ai_reply(
    category_id: UUID,
    request: MessageRequest,
    verified_user: VerifiedUser = Depends(verify_user),
    db_client: DBClient = Depends(getDBClient),
):
    return MessageService.get_ai_reply(
        request=request,
        user=verified_user.requesting_user,
        db_client=db_client,
        rag=True,
        category_id=category_id,
    )
