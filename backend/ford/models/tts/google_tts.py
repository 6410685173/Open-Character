from .tts_interface import TTSInterface
from google.cloud import texttospeech

class GoogleTTS(TTSInterface):

    def __init__(self, **kwargs) -> None:
        
        self.model = texttospeech.TextToSpeechClient()

    def text_to_speech(self, message: str):
        input_text = texttospeech.SynthesisInput(text=message)

        # Note: the voice can also be specified by name.
        # Names of voices can be retrieved with client.list_voices().
        voice = texttospeech.VoiceSelectionParams(
            language_code="th-TH",
        )

        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.LINEAR16,
            speaking_rate=1
        )

        response = self.model.synthesize_speech(
            request={"input": input_text, "voice": voice, "audio_config": audio_config}
        )
        # The response's audio_content is binary.
        return response.audio_content

