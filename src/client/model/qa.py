# model/qa.py
from langchain_openai import ChatOpenAI

from src.client.model.config import LINKS_HASHMAP
from src.client.model.config import OPENAI_API_KEY, SYSTEM_PROMPT


def query_gen(init_query:str, chat_history: list) -> str:
    messages = (
        "\n".join([f"{msg['role']}: {msg['content']}" for msg in chat_history])
        if chat_history
        else ""
    )
    query = f"{SYSTEM_PROMPT}\n{messages}\nuser: {init_query}"
    return query

def response_gen(result: dict) -> dict:
    answer = result["result"]
    sources = [doc.metadata['source'] for doc in result["source_documents"]]
    map = LINKS_HASHMAP
    linked_sources = []
    for i in sources:
        i = "[" + i[14:-3] + "]" + "(" + map[i] + ")"
        linked_sources.append(i)
    response = {
        "answer": answer,
        "sources": linked_sources
    }
    response["answer"] = f"""{response["answer"]}

Sources: {response["sources"]}
"""
    return response

def llm(model_name: str = "gpt-4"):
    bot = ChatOpenAI(
        model=model_name,
        temperature=1,
        top_p=1,
        openai_api_key=OPENAI_API_KEY,
    )
    return bot

