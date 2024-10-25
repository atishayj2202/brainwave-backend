from starlette.responses import Response

from src.client.whatsapp import WhatsAppClient
from src.schema.whatsapp import GetUserMessageRequest, Message, parse_message

message_ids = set()
def handle_message(request: dict, wb_client: WhatsAppClient):
    try:
        request = GetUserMessageRequest(**request)
    except Exception as e:
        print("Unexpected Response")
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
            wb_client.send_message_with_heading(
                heading="AI Output",
                recipient=message.from_number,
                message="AI will be deployed soon",
            )
            wb_client.markReaction(
                recipient=message.from_number,
                message_id=message.id,
                emoji="✅",
            )
        except Exception as e:
            wb_client.send_message_with_heading(
                heading="⚠️ Oops, something went wrong!",
                recipient=message.from_number,
                message="I'm sorry, but an unexpected error occurred while processing your request. Our team has been notified, and we're working hard to resolve the issue.\n\nPlease try again later. If the problem persists, feel free to contact our support team for further assistance.\n\nThank you for your patience and understanding.",
            )
    return Response(status_code=200)