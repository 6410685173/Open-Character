from .asr_interface import ASRInterface
from openai import OpenAI


class OpenAIASR(ASRInterface):

    def __init__(self, **kwargs) -> None:
        self.client = OpenAI(api_key = kwargs["API_KEY"])  

    def speech_to_text(self):
        audio_file= open("/path/to/file/audio.mp3", "rb")
        transcription = self.client.audio.transcriptions.create(
            model="whisper-1", 
            file=audio_file
        )

        return transcription