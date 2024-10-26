from starlette.responses import Response

from src.client.database import DBClient
from src.client.legal_help import Model
from src.client.whatsapp import WhatsAppClient
from src.db.wa_history import WAMessage
from src.schema.whatsapp import GetUserMessageRequest, Message, parse_message

message_ids = set()


def handle_message(request: dict, wb_client: WhatsAppClient, db_client: DBClient):
    try:
        request = GetUserMessageRequest(**request)
    except Exception as e:
        print("Unexpected Response")
        print(request)
        return Response(status_code=200)
    messages: list[Message] = request.get_messages()
    if messages is not None:
        message = parse_message(messages[0])
        if message.id in message_ids:
            return Response(status_code=200)
        message_ids.add(message.id)
        if message.text.body is None:
            wb_client.send_message(
                recipient=message.from_number,
                message="Sorry, I can't process this message. Please provide normal text",
            )
            return Response(status_code=200)
        try:
            wb_client.markReaction(
                recipient=message.from_number,
                message_id=message.id,
                emoji="⏳",
            )
            message_history = []
            messages = db_client.query(
                WAMessage.get_by_field_multiple,
                field="wa_id",
                match_value=message.from_number,
                error_not_exist=False
            )
            if messages is not None:
                for i in messages:
                    message_history.append(
                        i.message,
                    )
                    message_history.append(
                        i.output_message
                    )
            model = Model()
            question = message.text.body
            new_message = WAMessage(
                message_id=message.id,
                message=question,
                output_message=model.chatbot(question, message_history)[-1][11:],
                wa_id=message.from_number
            )
            wb_client.send_message(
                recipient=message.from_number,
                message=new_message.output_message,
                context=message.id
            )
            wb_client.markReaction(
                recipient=message.from_number,
                message_id=message.id,
                emoji="✅",
            )
            db_client.query(
                WAMessage.add,
                items=[new_message]
            )
        except Exception as e:
            wb_client.send_message_with_heading(
                heading="⚠️ Oops, something went wrong!",
                recipient=message.from_number,
                message="I'm sorry, but an unexpected error occurred while processing your request. Our team has been notified, and we're working hard to resolve the issue.\n\nPlease try again later. If the problem persists, feel free to contact our support team for further assistance.\n\nThank you for your patience and understanding.",
            )
    return Response(status_code=200)
