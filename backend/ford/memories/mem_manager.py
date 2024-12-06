from ..models.llm.llm_interface import LLMInterface
import json
import os
import time
class MemomryManager:
    def __init__(self, method:str, id:str, limit_length:int=10,last_message:int=4, llm:LLMInterface=None) -> None:
        
        self.id = id
        self.method = method
        self.limit_length = limit_length
        self.last_message = last_message
        self.llm = llm

        try:
            
            with open(f"./ford/memories/ford_memory/{self.id}.json", 'r', encoding='utf-8') as f:
                self.__loaded_memmory:list[dict] = json.load(f)
                
        except:
            print(os.getcwd())
            self.__loaded_memmory:list[dict] = [] # empty memory

        self.memory:list[dict] = self.__loaded_memmory.copy() 
        self.summarization_prompt :str = """
Role: You are an AI assistant tasked with summarizing a conversation between a user and another AI, where the conversation may contain messages in multiple languages. Your goal is to provide a concise summary for each language used, capturing the key points discussed.

Instructions:
Given a conversation history , where each role contains a message and the assistant's corresponding response (in potentially different languages), perform the following steps:

1. Initialize two summary strings, one for the user messages and one for the assistant messages.
2. For each message pair:
   - Extract the user message and add it to the summary, prefaced with "User: ".
   - Extract the assistant's response and add it to the summary, prefaced with "Assistant: ".
   - Identify any important information or insights in the assistant's response, indicated. Extract those and add them to the summary.
3. Returns a brief summary of the conversation, highlighting the key points discussed.
Start with this not introduce first: This is a summary of the previous conversation between Ford.
"""
        # self.update_memory()


    def update_memory(self, user_message:dict|None=None, ford_message:dict|None=None):

        if len(self.memory) > self.limit_length:
            if self.method == "last_turn":
                self.memory = self.memory[-self.last_message:]
                
            elif self.method == "last_turn&summarization":
                print("summarize memory")
                time.sleep(3)
                
                if self.llm is not None:
                    summarize_conversation = self.llm.thinking(memory= [{"role":"user","content":"\n".join([f"{msg['role']}:msg{msg['content']}" for msg in self.memory[:-self.last_message]])}], role_prompt=self.summarization_prompt, stream=False)
                    
                    self.memory = [{"role":"user","content":summarize_conversation["content"][0].text}]+self.memory[-self.last_message:]
                    print(self.memory)
                else:
                    raise Exception("Require LLM to summarize conversation")
               
        if (user_message is not None) and (ford_message is not None):
            self.memory.extend([user_message,ford_message])
            self.__loaded_memmory.extend([user_message,ford_message])
   
            self.save_memory()


    def save_memory(self)-> None:
        try:
            with open(f"./ford/memories/ford_memory/{self.id}.json", "w", encoding='utf-8') as outfile:
                json.dump(self.__loaded_memmory, outfile, indent=4)

        except Exception as e:
            print(e)

    def get_memory(self)-> None:
        return self.__loaded_memmory