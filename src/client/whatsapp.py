import os

import requests


class WhatsAppClient:
    __ACCESS_TOKEN = os.environ["WHATSAPP_TOKEN"]
    __headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {__ACCESS_TOKEN}",
    }
    __ACCOUNT_SID = os.environ["WHATSAPP_APP_ID"]
    __BASE_URL = os.environ["WHATSAPP_URL"] + __ACCOUNT_SID

    @classmethod
    def __send(cls, data: dict, message: str) -> dict:
        response: dict = requests.post(
            cls.__BASE_URL + "/messages", headers=cls.__headers, json=data
        ).json()
        print(response)
        return response

    @classmethod
    def send_message(cls, message: str, recipient: str, footer: str | None = None, context: str | None = None) -> dict:
        if message.endswith('\n'):
            message = message[:-1]
        if footer is not None:
            message += f"\n> {footer}"
        data = {
            "messaging_product": "whatsapp",
            "to": recipient,
            "type": "text",
            "text": {"body": message},
        }
        if context is not None:
            data["context"] = {
                "message_id": context,
            }
        return cls.__send(
            data,
            message,
        )

    @classmethod
    def send_message_with_heading(
            cls, message: str, recipient: str, heading: str, footer: str = None
    ) -> dict:
        if message.endswith('\n'):
            message = message[:-1]
        if footer is not None:
            message += f"\n> {footer}"
        data = {
            "messaging_product": "whatsapp",
            "to": recipient,
            "type": "text",
            "text": {"body": "*" + heading + "*\n\n" + message},
        }
        return cls.__send(
            data,
            "*" + heading + "*\n\n" + message,
        )

    @classmethod
    def reduce_text_len(cls, text: str) -> str:
        if len(text) > 23:
            return text[:20] + "..."
        return text

    @classmethod
    def send_message_with_quick_reply(
            cls, message: str, recipient: str, quick_reply: list[str], heading: str, footer: str = None
    ) -> dict:
        if message.endswith('\n'):
            message = message[:-1]
        if footer is not None:
            message += f"\n> {footer}"
        if len(quick_reply) == 0:
            return cls.send_message("Options Not Found", recipient)
        data = {
            "messaging_product": "whatsapp",
            "to": recipient,
            "type": "interactive",
            "interactive": {
                "type": "list",
                "body": {"text": message},
                "action": {
                    "button": heading,
                    "sections": [
                        {
                            "title": "SECTION_1_TITLE",
                            "rows": [
                                {
                                    "id": i,
                                    "title": cls.reduce_text_len(i),
                                }
                                for i in quick_reply
                            ],
                        }
                    ],
                },
            },
        }
        return cls.__send(
            data,
            f"{message}\n{', '.join(quick_reply)}",
        )

    @classmethod
    def send_message_with_reply_list(
            cls, message: str, recipient: str, quick_reply: dict[str, str], heading: str, footer: str = None
    ) -> dict:
        if message.endswith('\n'):
            message = message[:-1]
        if footer is not None:
            message += f"\n> {footer}"
        if len(quick_reply) == 0:
            return cls.send_message("Options Not Found", recipient)
        data = {
            "messaging_product": "whatsapp",
            "to": recipient,
            "type": "interactive",
            "interactive": {
                "type": "list",
                "body": {"text": message},
                "action": {
                    "button": heading,
                    "sections": [
                        {
                            "title": "SECTION_1_TITLE",
                            "rows": [
                                {
                                    "id": i,
                                    "title": cls.reduce_text_len(i),
                                    "description": quick_reply[i],
                                }
                                for i in quick_reply
                            ],
                        }
                    ],
                },
            },
        }
        return cls.__send(
            data,
            f"{message}\n{', '.join(quick_reply)}",
        )

    @classmethod
    def send_pdf(cls, pdf_url: str, recipient: str, text: str, file_name: str, footer: str = None) -> dict:
        if text.endswith('\n'):
            text = text[:-1]
        if footer is not None:
            text += f"\n> {footer}"
        data = {
            "messaging_product": "whatsapp",
            "to": recipient,
            "type": "document",
            "document": {
                "link": pdf_url,
                "filename": file_name,
                "caption": text,
            },
        }
        return cls.__send(
            data,
            text,
        )

    @classmethod
    def markReaction(cls, recipient: str, message_id: str, emoji: str) -> dict:
        data = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": recipient,
            "type": "reaction",
            "reaction": {
                "message_id": message_id,
                "emoji": emoji,
            },
        }
        return cls.__send(
            data,
            message_id + emoji,
        )

    @classmethod
    def sendFlow(
            cls,
            recipient: str,
            flow_id: str,
            body: str,
            flow_token: str,
            button_text: str,
            start_screen_id: str,
            footer: str = None,
    ) -> dict:
        if body.endswith('\n'):
            body = body[:-1]
        if footer is not None:
            body += f"\n> {footer}"
        data = {
            "recipient_type": "individual",
            "messaging_product": "whatsapp",
            "to": recipient,
            "type": "interactive",
            "interactive": {
                "type": "flow",
                "body": {"text": body},
                "action": {
                    "name": "flow",
                    "parameters": {
                        "flow_message_version": "3",
                        "flow_token": flow_token,
                        "flow_id": flow_id,
                        "flow_cta": button_text,
                        "flow_action": "navigate",
                        "flow_action_payload": {"screen": start_screen_id},
                    },
                },
            },
        }
        return cls.__send(
            data,
            body,
        )

    @classmethod
    def markSeen(cls, message_id: str) -> dict:
        data = {
            "messaging_product": "whatsapp",
            "status": "read",
            "message_id": message_id,
        }
        response = requests.post(
            cls.__BASE_URL + "/messages", headers=cls.__headers, json=data
        ).json()
        return response


if __name__ == "__main__":
    WhatsAppClient.send_message_with_quick_reply(
        message="Please select an option:",
        recipient="917701958417",
        quick_reply=[
            "Attendance Summary",
            "Subject-wise Attendance",
            "Admit Card",
            "Student Transcript",
            "Sign Out",
            "Remember Password",
        ],
        heading="Select an Option",
    )
