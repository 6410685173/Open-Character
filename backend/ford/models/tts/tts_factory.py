from .tts_interface import TTSInterface

class TTSFactory:
    
    def get_tts_model(self, model_name:str = "GOOGLE_TTS", **kwargs) -> TTSInterface:

        if model_name == "GOOGLE_TTS":
            from .google_tts import GoogleTTS

            return GoogleTTS(**kwargs)

        elif model_name == "OpenAI_TTS":
            from .openai_tts import OpenAI_TTS

            return OpenAI_TTS(**kwargs)