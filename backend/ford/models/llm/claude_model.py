from anthropic import AnthropicVertex
from .llm_interface import LLMInterface


class ClaudeModel(LLMInterface):

    def __init__(self, tools:list[dict]|None = None, **kwargs):

        self.model = AnthropicVertex(project_id=kwargs["PROJECT_ID"],
                                     region=kwargs["REGION"])
        self.version:str = kwargs["MODEL_VERSION"]
        self.tools = tools
    

    def thinking(self, memory:list[dict], role_prompt:str, stream:bool):
        
        if stream:
            def thinking_iterator():
                with self.model.messages.stream(
                    model=self.version,
                    max_tokens=1000,
                    system=role_prompt,
                    tools=self.tools,
                    messages=[{"role":data["role"],"content":data["content"]} for data in memory],
                ) as result:
                    for text in result.text_stream:
                        yield text  
                
            return thinking_iterator()  # Return the iterator
        
        else:
            try:
                response = self.model.messages.create(
                    model=self.version,
                    max_tokens=1000,
                    system=role_prompt,
                    tools=self.tools,
                    messages=[{"role": data["role"], "content": data["content"]} for data in memory]
                )
                
                return {
                    "stop_reason": response.stop_reason,
                    "tool_use": next((block for block in response.content if block.type == "tool_use"), None),
                    "content": response.content
                }
            
            except Exception as e:
                # Handle any API errors
                print(f"Error in get_response: {str(e)}")
                raise
            
    



    
        
            

    
