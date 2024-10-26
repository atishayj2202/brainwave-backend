from uuid import UUID

from starlette.exceptions import HTTPException

from src.client.database import DBClient
from src.client.model import Model
from src.client.model_hi import Model as HModel
from src.db.message import Message
from src.db.user import User
from src.schema.message import MessageRequest, MessageResponse, SoundResponse


class MessageService:

    @classmethod
    def get_all_messages(
        cls, user: User, db_client: DBClient, category_id: UUID = None
    ) -> list[MessageResponse]:
        messages = db_client.query(
            Message.get_by_multiple_field_multiple,
            fields=["user_id", "category_id"],
            match_values=[user.id, category_id],
            error_not_exist=False,
        )
        if messages is None:
            return []
        return [
            MessageResponse(
                message=message.message if message.hindi_message is None else message.hindi_message,
                role=message.role,
                message_id=message.id,
                created_at=message.created_at,
            )
            for message in messages
        ]

    @classmethod
    def get_ai_reply(
        cls,
        request: MessageRequest,
        user: User,
        db_client: DBClient,
        rag: bool = True,
        category_id: UUID = None,
    ) -> MessageResponse:
        question = Message(
            message=request.question,
            user_id=user.id,
            role="User",
            status="Pending",
            category_id=category_id,
        )
        question.status = "Done"
        temp = db_client.query(
            Message.get_by_multiple_field_multiple,
            fields=["user_id", "category_id"],
            match_values=[user.id, category_id],
            error_not_exist=False,
        )
        messages = []
        '''if temp is not None:
            for message in temp:
                messages.append(
                    {
                        "role": "assistant" if message.role == "AI" else "user",
                        "content": [{"type": "text", "text": message.message}],
                    }
                )
        '''
        if temp is not None:
            for message in temp:
                messages.append(
                    message.message
                )
        model = Model()

        if rag:
            #temp = model.chatbot(request.question, messages)
            #sources = temp["sources"]
            #ans = temp["answer"]
            sources = None
            ans = model.chatbot(request.question, messages)[-1]
            ans = ans[11:]
        else:
            ans = model.chatbot(
                request.question,
                messages,
            )[-1]
            ans = ans[11:]
            sources = None
        answer = Message(
            message=ans,
            user_id=user.id,
            role="AI",
            status="Done",
            category_id=category_id,
        )
        db_client.query(Message.add, items=[question, answer])
        return MessageResponse(
            message=answer.message,
            role=answer.role,
            message_id=answer.id,
            created_at=answer.created_at,
            sources=sources,
        )

    @classmethod
    def get_hindi_ai_reply(
        cls,
        request: MessageRequest,
        user: User,
        db_client: DBClient,
        category_id: UUID = None,
    ) -> MessageResponse:
        question = Message(
            message=request.question,
            user_id=user.id,
            role="User",
            status="Pending",
            category_id=category_id,
        )
        question.status = "Done"
        temp = db_client.query(
            Message.get_by_multiple_field_multiple,
            fields=["user_id", "category_id"],
            match_values=[user.id, category_id],
            error_not_exist=False,
        )
        messages = []
        hindi_messages = []
        if temp is not None:
            for message in temp:
                messages.append(
                    message.message
                )
                if message.hindi_message is not None:
                    hindi_messages.append(
                        message.hindi_message
                    )
                else:
                    hindi_messages.append(
                        ""
                    )
        model = HModel()
        ans, ans_h = model.chatbot(request.question, messages, hindi_messages)
        ans = ans[-1]
        ans_h = ans_h[-1]
        answer = Message(
            message=ans,
            user_id=user.id,
            role="AI",
            status="Done",
            category_id=category_id,
            hindi_message=ans_h,
        )
        db_client.query(Message.add, items=[question, answer])
        return MessageResponse(
            message=ans_h,
            role=answer.role,
            message_id=answer.id,
            created_at=answer.created_at,
            sources=[ans],
        )

    @classmethod
    def get_sound(
        cls,
        message_id: UUID,
        db_client: DBClient,
    ) -> SoundResponse:
        message: Message | None = db_client.query(
            Message.get_id,
            id=message_id,
            error_not_exist=False
        )
        if message is None:
            raise HTTPException(status_code=404, detail="Message not found")
        text = message.message if message.hindi_message is None else message.hindi_message
        return SoundResponse(
            sound_url="atishayj.me",
            message_id=message.id,
            message=text,
        )

