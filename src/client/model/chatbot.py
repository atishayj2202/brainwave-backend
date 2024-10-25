from openai import OpenAI

from src.client.model.config import OPENAI_API_KEY, SYSTEM_PROMPT_2

model = OpenAI(api_key=OPENAI_API_KEY)


def chatbot(messages: list, model_name: str="gpt-4"):
    system_prompt = {
                    "role": "system",
                    "content": [
                        {
                            "type": "text",
                            "text": SYSTEM_PROMPT_2
                        }
                    ],
                }
    if messages[0] != system_prompt:
        messages.insert(0, system_prompt)
    chat = model.chat.completions.create(
        model=model_name,
        temperature=1,
        max_tokens=2048,
        top_p=1,
        messages=messages,
        frequency_penalty=0,
        presence_penalty=0,
        response_format={"type": "text"},
    )
    return chat
