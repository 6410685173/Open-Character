from .tts_interface import TTSInterface
from openai import OpenAI

class OpenAI_TTS(TTSInterface):

    def __init__(self, **kwargs) -> None:
        self.client = OpenAI(api_key = kwargs["API_KEY"])  
        self.model = kwargs["MODEL"]
        self.voice = kwargs["VOICE"]
        

    def text_to_speech(self, message: str):
        response = self.client.audio.speech.create(
            model=self.model,
            voice=self.voice,
            input=message,
        )

        return response





