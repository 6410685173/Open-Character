from .asr_interface import ASRInterface
from google.cloud.speech_v2 import SpeechClient
from google.cloud.speech_v2.types import cloud_speech

class GoogleASR(ASRInterface):

    def __init__(self, **kwargs) -> None:
        super().__init__()
        self.client = SpeechClient()
        self.config = cloud_speech.RecognitionConfig(
            auto_decoding_config=cloud_speech.AutoDetectDecodingConfig(),
            language_codes=["th-TH"], #"th-TH"
            model="long",
        )
        self.PROJECT_ID = kwargs["PROJECT_ID"]
        

    def speech_to_text(self, audio_content) -> str:
        """Transcribe an audio file.
        Args:
            audio_file 
        Returns:
            String : from cloud_speech.RecognizeResponse The response from the recognize request, containing
            the transcription results
        """

        request = cloud_speech.RecognizeRequest(
            recognizer=f"projects/{self.PROJECT_ID}/locations/global/recognizers/_",
            config=self.config,
            content=audio_content,
        )

        # Transcribes the audio into text
        response = self.client.recognize(request=request)

        for result in response.results:
            print(f"Transcript: {result.alternatives[0].transcript}")
            return result.alternatives[0].transcript


    

    

    

    