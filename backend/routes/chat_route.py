from fastapi import APIRouter, Body
import yaml
import os
import uuid


# for testing
def setup_chat_route(router:APIRouter):

    with open('./engine_config.yaml', 'r', encoding='utf-8') as file:
        config = yaml.safe_load(file)
        
    
    @router.get("/get_all_chat")
    def get_chat_endpoint():
        return [m.strip(".json") for m in os.listdir("./ford/memories/ford_memory")]
    
    @router.post("/new_chat")
    def new_chat_endpoint():
        id_memory = str(uuid.uuid4())
        with open(f'./ford/memories/ford_memory/{id_memory}.json', 'w') as fp:
            return id_memory
        
    @router.post("/del_chat")
    def del_chat_endpoint(id = Body(..., embed=True)):
        try:
            os.remove(f"./ford/memories/ford_memory/{id}.json")
        except Exception as e:
            print("there is no this conversation")


