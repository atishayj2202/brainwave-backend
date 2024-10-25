from src.client.legal_help.chatbot import chat
from src.client.legal_help.config import system_prompt

class Model:
    def __init__(self) -> None:
        self.system_prompt = system_prompt

    def chatbot(self, query: str, history: list[str]) -> list[str]:
        sys = self.system_prompt
        if history == [] or history[0] != sys:
            history.insert(0, sys)
        history.append("user: " + query)
        final_query = ""
        for i in history:
            final_query += i + "\n"
        response = chat(final_query)
        history.append("assistant: " + response)
        return history
