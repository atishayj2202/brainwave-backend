import json
from abc import ABC
from datetime import datetime

from pydantic import BaseModel, Field


class _Base(ABC, BaseModel):
    def dict(self, **kwargs):
        default_dict = super().dict(**kwargs)
        if "from_number" in default_dict:
            default_dict["from"] = default_dict.pop("from_number")
        return {key: value for key, value in default_dict.items() if value is not None}


class Profile(_Base):
    name: str


class PhoneNumber(_Base):
    profile: Profile
    wa_id: str


class TextMessage(_Base):
    body: str | dict | None = None


class ListReply(_Base):
    id: str
    title: str
    description: str | None = None


class NfmReply(_Base):
    name: str
    body: str
    response_json: dict | str


class InteractiveMessage(_Base):
    type: str
    list_reply: ListReply | None = None
    nfm_reply: NfmReply | None = None


class Context(_Base):
    id: str
    from_number: str = Field(..., alias="from")


class Message(_Base):
    from_number: str = Field(..., alias="from")
    id: str
    context: Context | None = None
    timestamp: str
    type: str
    text: TextMessage | None = None
    interactive: InteractiveMessage | None = None

    def get_timestamp_utc(self):
        return datetime.utcfromtimestamp(int(self.timestamp))

    def get_text(self):
        # return text as per message type
        if self.text:
            return self.text.body
        elif self.button:
            return self.button.text
        else:
            return None

    def get_parent_id(self):
        if self.context:
            return self.context.id
        else:
            return None


class Origin(_Base):
    type: str


class Conversation(_Base):
    id: str
    expiration_timestamp: str | None = ""
    origin: Origin


class Pricing(_Base):
    billable: bool
    pricing_model: str
    category: str


class Status(_Base):
    id: str
    status: str
    timestamp: str
    recipient_id: str
    conversation: Conversation | None
    pricing: Pricing | None


class Metadata(_Base):
    display_phone_number: str
    phone_number_id: str


class Value(_Base):
    messaging_product: str
    metadata: Metadata
    contacts: list[PhoneNumber] | None = None
    messages: list[Message] | None = None
    statuses: list[Status] | None = None

    def get_messages(self):
        if self.messages:
            return self.messages
        else:
            return None


class Change(_Base):
    value: Value
    field: str


class Entry(_Base):
    id: str
    changes: list[Change]


class ParsedProfile(BaseModel):
    name: str
    wa_id: str | None
    display_phone_number: str | None
    phone_number_id: str | None


class GetUserMessageRequest(BaseModel):
    object: str
    entry: list[Entry]

    def get_messages(self) -> list[Message]:
        return self.entry[0].changes[0].value.get_messages()

    def get_profile(self) -> ParsedProfile:
        value = self.entry[0].changes[0].value
        return ParsedProfile(
            name=value.contacts[0].profile.name,
            wa_id=value.contacts[0].wa_id,
            display_phone_number=value.metadata.display_phone_number,
            phone_number_id=value.metadata.phone_number_id,
        )

    def get_status(self) -> list[Status]:
        value = self.entry[0].changes[0].value
        return value.statuses


def parse_message(message: Message) -> Message:
    if message.interactive is None and message.text is None:
        message.text = TextMessage(body=None)
        return message
    if message.interactive is not None and message.text is None:
        if message.interactive.list_reply is not None:
            message.text = TextMessage(body=message.interactive.list_reply.id)
        else:
            temp = message.interactive.nfm_reply
            if type(temp.response_json) is str:
                temp.response_json = json.loads(temp.response_json)
            message.text = TextMessage(body=temp.response_json)
        return message
    return message
