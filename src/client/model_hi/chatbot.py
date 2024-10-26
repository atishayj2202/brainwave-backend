import requests

from src.client.model_hi.config import external_user_id, api_key

create_session_url = "https://api.on-demand.io/chat/v1/sessions"
create_session_headers = {"apikey": api_key}
create_session_body = {"pluginIds": [], "externalUserId": external_user_id}

response = requests.post(
    create_session_url, headers=create_session_headers, json=create_session_body
)
response_data = response.json()
session_id = response_data["data"]["id"]
submit_query_url = f"https://api.on-demand.io/chat/v1/sessions/{session_id}/query"
submit_query_headers = {"apikey": api_key}


def chat(query: str) -> str:
    submit_query_body = {
        "endpointId": "predefined-openai-gpt4o",
        "query": query,
        "pluginIds": ["plugin-1726226353", "plugin-1729856480"],
        "responseMode": "sync",
    }

    query_response = requests.post(
        submit_query_url, headers=submit_query_headers, json=submit_query_body
    )
    query_response_data = query_response.json()

    return query_response_data["data"]["answer"]
