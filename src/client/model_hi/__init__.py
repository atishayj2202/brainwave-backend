from src.client.model_hi.chatbot import chat
from src.client.model_hi.config import system_prompt
from src.client.model_hi.translate import translate


class Model:
    def __init__(self) -> None:
        self.system_prompt = system_prompt

    def chatbot(
            self, query: str, history: list[str], history_hi: list[str]
    ) -> tuple[list[str], list[str]]:
        sys = self.system_prompt
        if history == [] or history[0] != sys:
            history.insert(0, sys)
        history.append("user: " + query)
        final_query = ""
        for i in history:
            final_query += i + "\n"
        response = chat(final_query)
        history.append("assistant: " + response)
        history_hi.append(translate(response))
        return history, history_hi

