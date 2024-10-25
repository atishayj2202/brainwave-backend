from langchain.chains.retrieval_qa.base import RetrievalQA
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

from src.client.model.chatbot import chatbot
from src.client.model.config import SYSTEM_PROMPT_2, MARKDOWN_PATH, OPENAI_API_KEY, FAISS_INDEX_PATH
from src.client.model.qa import llm, query_gen, response_gen
from src.client.model.retriever import get_retriever


class RAG_Model:
    def __init__(self):
        pass

    def ingest_documents(self) -> None:
        loader = DirectoryLoader(MARKDOWN_PATH, glob="**/*.md")
        documents = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        docs = text_splitter.split_documents(documents)

        embeddings = OpenAIEmbeddings(
            model="text-embedding-ada-002", openai_api_key=OPENAI_API_KEY
        )
        vector_store = FAISS.from_documents(docs, embeddings)
        vector_store.save_local(FAISS_INDEX_PATH)

    def prompt(self, question, chat_history: list) -> dict:
        model = llm()

        retriever = get_retriever()

        qa_chain = RetrievalQA.from_chain_type(
            llm=model, chain_type="stuff", retriever=retriever, return_source_documents=True
        )

        full_query = query_gen(question, chat_history)

        result = qa_chain.invoke({"query": full_query})

        response = response_gen(result)
        return response


class ChatBot:
    def __init__(self):
        pass

    def prompt(self, question: str, messages: list) -> str:
        if question:
            messages.append(
                {"role": "user", "content": question},
            )
            chat = chatbot(messages)
        else:
            return "Unexpected error"
        response = chat.choices[0].message.content
        return response