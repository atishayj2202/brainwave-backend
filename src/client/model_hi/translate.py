import requests
from src.client.model_hi.config import api_key

url = "https://api.on-demand.io/services/v1/public/service/execute/language_translation"

def translate(text: str) -> str:
    payload = {
        "input": text,
        "languageCode": "hi"
    }
    headers = {
        "accept": "application/json",
        "apikey": api_key,
        "content-type": "application/json",
    }

    response = requests.post(url, json=payload, headers=headers)

    final_response = response.json()
    return final_response["data"]["translatedText"]