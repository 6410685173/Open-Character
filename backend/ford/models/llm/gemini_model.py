import google.generativeai as genai
from .llm_interface import LLMInterface



class GeminiModel(LLMInterface):

    def __init__(self, **kwargs):
        genai.configure(api_key=kwargs["GEMINI_API_KEY"])
        self.model = genai.GenerativeModel(
                        model_name=kwargs["MODEL_VERSION"],
                    )
    

    def thinking(self, memory:list[dict], role_prompt:str, stream:bool):
        
        if stream:
            # def thinking_iterator():
            #     with self.model.messages.stream(
            #         model=self.version,
            #         max_tokens=1000,
            #         system=role_prompt,
            #         messages=[{"role":data["role"],"content":data["content"]} for data in memory],
            #     ) as result:
            #         for text in result.text_stream:
            #             yield text  
                
            # return thinking_iterator()  # Return the iterator
            pass
        else:
            self.model._system_instruction = role_prompt
            response = self.model.generate_content(
                contents=[{"role":"model", "parts":role_prompt}]+[ {"role":d["role"] if d["role"]=="user" else "model", "parts":d["content"]} for d in memory],
                generation_config = {
                    "max_output_tokens": 8192,
                    "response_mime_type": "application/json",
                }
            )
            
            

            return response
    
    
    # def _function_calling(self, memory:list[dict], role_prompt:str):
    #     pass