from .asr_interface import ASRInterface


class ARSFactory:

    def get_asr_model(self, model_name:str="GOOGLE_ASR", **kwargs) -> ASRInterface:

        if model_name == "GOOGLE_ASR":
            from .google_asr import GoogleASR

            return GoogleASR(**kwargs)
        
        if model_name == "OpenAI_ASR":
            from .openai_asr import OpenAIASR

            return OpenAIASR(**kwargs)