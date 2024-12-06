from .models.asr import ASRInterface, ARSFactory
from .models.llm import LLMInterface, LLMFactory
from .models.tts import TTSInterface, TTSFactory
from .memories.mem_manager import MemomryManager
from bs4 import BeautifulSoup
import json
import uuid
import re
import requests
import time

class AICharacter:

    def __init__(self, id:str, configs:dict=None) -> None:
        self.config = configs
        self.ability = [
            {
                "name": "get_calendar",
                "description": "Retrieves the calendar availability based on the specified date. Returns whether the time slot is free or not free.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "date": {
                            "type": "string",
                            "description": "The day of the week (e.g., 'Monday', 'Tuesday', etc.)."
                        },
                    },
                    "required": ["date"]
                }
            },
            {
                "name": "google_search",
                "description": "Pulls data from websites that use Google search and returns the content of the website. Use when the user asks for a search or the assistant does not know and uses Google to search for information.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "date": {
                            "type": "string",
                            "description": "query for searching google "
                        },
                    },
                    "required": ["query"]
                }
            }
        ]
        self.id = id
        self.brain:LLMInterface = self._init_llm()
        self.ears:ASRInterface = self._init_asr()
        self.mouth:TTSInterface = self._init_tts()
        self.memories:MemomryManager = self._init_memory()
           
    
    # recieve voice or text from user
    def listen(self, voice):
        return self.ears.speech_to_text(voice)
    

    def __get_ability(self, name_function, func_input):

        if name_function == "google_search":
            return self.__google_search(func_input["query"])
        
        elif name_function == "get_calendar":
            return self.__get_calendar(func_input["date"])


    def thinking(self, message:str, stream:bool=True, memorize:bool=True):
        
        if stream:
            return self.brain.thinking(memory= self.memories.memory, role_prompt=self.config["ROLE_PROMPT"], stream=True) 
        
        else:
        

            output  = self.brain.thinking(memory=self.memories.memory+[{
                                                    "role": "user", 
                                                    "content": message, #.join('\n Respond any question in the following json format.{ "content": "<your response>", "mood": Mood to choose, "background": Background to choose }')
                                                }], 
                                          role_prompt=self.config["ROLE_PROMPT"], 
                                          stream=False)
            
            print(output)
            while output["stop_reason"] == "tool_use" and output["tool_use"]:
                tool_name = output["tool_use"].name
                tool_input = output["tool_use"].input

                tool_result = self.__get_ability(tool_name, tool_input)

                # turn message for function calling
                messages_tool_call = [
                    {"role": "user", "content": message},
                    {"role": "assistant", "content": output["content"]},
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "tool_result",
                                "tool_use_id": output["tool_use"].id,
                                "content": str(tool_result),
                            }
                        ],
                    },
                ]
                time.sleep(3)
                output = self.brain.thinking(memory= self.memories.memory + messages_tool_call, role_prompt=self.config["ROLE_PROMPT"], stream=stream)

            
            json_match = re.search(r'<answer>\s*(\{.*\})\s*</answer>', output["content"][0].text, re.DOTALL)
        
    
            if json_match:
                json_text = json_match.group(1).strip()  # Extract JSON string within tags and remove any extra whitespace

                try:
                    # Parse JSON string to confirm it's valid JSON
                    json_data = json.loads(json_text)
                    
                except json.JSONDecodeError:
                    print("Error: Extracted text is not valid JSON.")
                    # Extract answer
                    answer_match = re.search(r'content\s*"(.*?)"(?=\s*mood)', output["content"][0].text, re.DOTALL)
                    # Extract mood
                    mood_match = re.search(r'"mood"\s*:\s*"([^"]*)"', output["content"][0].text, re.DOTALL)
                    # Extract background
                    background_match = re.search(r'"background"\s*:\s*"([^"]*)"', output["content"][0].text, re.DOTALL)

                    json_data = {
                        "content": answer_match.group(1) if answer_match else output["content"][0].text,
                        "mood": mood_match.group(1) if mood_match else "general",
                        "background": background_match.group(1) if background_match else "general"
                    }
                    print(json_data)
                    pass
                    
            else:
                print("No <answer> tag found.") # handle halucination llm to force mood and background
                json_data = {
                    "content":output["content"][0].text,
                    "mood":None,
                    "background":None
                }

            user_message = {
                "id": str(uuid.uuid4()),
                "role": "user", 
                "content": message,
            }

            response = {
                "id": str(uuid.uuid4()),
                "role": "assistant",
                "content": json_data["content"],
                "mood": json_data["mood"],
                "background": json_data["background"]
            }

            if memorize:
                self._update_memmory(user = user_message, assistant=response)

            return response
            

    def speak(self, text:str, stream:bool, id:str=None):
        if not stream:
            # The response's audio_content is binary.
            response = self.mouth.text_to_speech(text)
            with open(f"./ford/voices/{id}.mp3", "wb") as out:
                out.write(response)
                print(f'Audio content is saved as memory {id}.mp3')
            return  response # for simple improve later


    def get_memory(self):
        return self.memories.get_memory()
    

    def get_voice(self, id):
        with open(f"./ford/voices/{id}.mp3", "rb") as out:    
            return out.read()
    

    def _update_memmory(self, user:dict, assistant:dict):
        self.memories.update_memory(
            user_message= user,
            ford_message= assistant,
        )

    


    def _init_llm(self) -> LLMInterface:
        factory = LLMFactory()
        
        llm = factory.get_llm_model(model_name=self.config["LLM_MODEL"], **self.config[self.config["LLM_MODEL"]])
        llm.tools = self.ability
        return llm

    def _init_asr(self) -> ASRInterface:
        factory = ARSFactory()
        
        return factory.get_asr_model(model_name=self.config["ASR_MODEL"], **self.config[self.config["ASR_MODEL"]])

    def _init_tts(self) -> TTSInterface:
        factory = TTSFactory()
        
        return factory.get_tts_model(model_name=self.config["TTS_MODEL"], **self.config[self.config["TTS_MODEL"]])

    def _init_memory(self):
        return MemomryManager(method="last_turn",id=self.id, llm=self.brain,limit_length=30)


    
    def __google_search(self, query: str) -> str:
        """
        Perform a Google search using the Custom Search JSON API.
        
        Parameters:
            query (str): The search query.

        Returns:
            content in website
        """

        def fetch_web_content(url: str) -> str:
            try:
                # Fetch the HTML content
                response = requests.get(url)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'html.parser')
                # Extract text based on known structure of the target page
                content = []
                
                # Customize these selectors as per the HTML structure
                # For example: main content within divs with a specific class
                for div in soup.find_all('div'):  # Adjust 'specific-content-class'
                    content.append(div.get_text(separator=' ', strip=True))
            
                
                # Join all parts into a single string of text
                main_text = '\n'.join(content)
                return main_text if main_text else "No relevant content found."
            
            except requests.exceptions.RequestException as e:
                return f"Error fetching content: {e}"

        search_url = "https://www.googleapis.com/customsearch/v1"
        params = {
            "key": self.config["GOOGLE_SEARCH"]["API_KEY"],
            "cx": self.config["GOOGLE_SEARCH"]["SEARCH_ENGINE_ID"],
            "q": query,
            "num": self.config["GOOGLE_SEARCH"]["NUM_RESULT"]
        }

        try:
            response = requests.get(search_url, params=params)
            response.raise_for_status()
            results = response.json().get("items", [])
            
            # Extract relevant information from each result
            search_results = []
            for item in results:
                result = {
                    "title": item.get("title"),
                    "link": item.get("link"),
                    "snippet": item.get("snippet")
                }
                search_results.append(result)
                
            return fetch_web_content(search_results[0]["link"])

        except requests.RequestException as e:
            print(f"An error occurred: {e}")
            return None

    def __get_calendar(self, date:str ) -> str:
        # mock up data
        print(date)
        calendar_data = {
            "monday": {
                "ไม่ว่างเรียนทั้งวัน"
            },
            "tuesday": {
                "ไม่ว่างเรียน TU108 ตอนเย็นก็มี วิชาภาคจนถึง 19.30 PM"
            },
            "wednesday": {
                "เรียนเช้า ว่างบ่าย"
            },
            "thursday": {
                "เรียนเช้า บ่ายเรียนสัมมนา"
            },
            "friday": {
                "เรียนเช้า ว่างบ่าย"
            },
            "saturday": {
                "ว่างทั้งวันเลย"
            },
            "sunday": {
                "ว่างทั้งวันเลย"
            }
        }

        return calendar_data.get(date.lower(), "i still dont know what i am gonna do")


if __name__ == "__main__":
    model = AICharacter()
    model.thinking("Send me a recipe for banana bread")