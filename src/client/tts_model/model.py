import requests


def model(input: str, voice: str = "onyx") -> requests.post:
    url = "https://api.on-demand.io/services/v1/public/service/execute/text_to_speech"
    payload = {
        "model": "tts-1-hd",
        "voice": voice,
        "input": input,
    }
    headers = {
        "accept": "application/json",
        "apikey": "nH43Asq7tCfkWTLPDlq4AD6qbzPY4NFT",
        "content-type": "application/json",
    }

    response = requests.post(url, json=payload, headers=headers)
    return response