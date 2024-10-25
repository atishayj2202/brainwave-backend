import os
from src.client.model.chatbot import chat
from src.client.model.config import system_prompt


class Model:
    def __init__(self) -> None:
        self.system_prompt = system_prompt

    def chatbot(self, query: str,  history: list[str]) -> list[str]:
        sys = self.system_prompt
        if history[0] != sys:
            history.insert(0, sys)
        history.append("user: "+query)
        response = chat(query)
        history.append("assistant: "+response)
        return history
