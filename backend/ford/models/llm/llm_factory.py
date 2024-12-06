from .llm_interface import LLMInterface

class LLMFactory:
    
    def get_llm_model(self, model_name:str = "CLAUDE", **kwags) -> LLMInterface:

        if model_name == "CLAUDE":
            from .claude_model import ClaudeModel
            
            return ClaudeModel(**kwags)
        
        elif model_name == "GEMINI":
            from .gemini_model import GeminiModel
            
            return GeminiModel(**kwags)
        