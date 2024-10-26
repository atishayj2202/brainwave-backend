from src.client.tts_model.model import model

class TTS_Model:
    def __init__(self):
        pass

    def tts(self, text: str) -> str:
        response = model(text).json()
        final_response = response["data"]["audioUrl"]
        return final_response