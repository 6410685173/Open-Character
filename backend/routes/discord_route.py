from fastapi import APIRouter, UploadFile, HTTPException, Body, File
from fastapi.responses import FileResponse
from fastapi.responses import JSONResponse
from ford.AIEngine import AICharacter
import yaml
import base64



def setup_discord_route(router:APIRouter):

    with open('./engine_config.yaml', 'r', encoding='utf-8') as file:
        config = yaml.safe_load(file)
        
    @router.post("/chat_endpoint")
    def chat_endpoint(msg = Body(..., embed=True)):

        ford = AICharacter(id="discord_test", configs=config)
        response = ford.thinking(msg, False)
        ford.speak(response["content"], stream=False, id=response["id"])
        return response
    
    @router.post("/talk_endpoint")
    async def talk_endpoint(audio = Body(..., embed=True)):
        
         # Read the uploaded file content

        try:
            decoded_audio = base64.b64decode(audio)
            ford = AICharacter(id="discord_test", configs=config)
            text = ford.listen(voice=decoded_audio)
            response = ford.thinking(text, False)
            ford.speak(response["content"], stream=False, id=response["id"])
            return response

        except Exception as e:
            print(e)

    @router.get("/get_voice_endpoint")
    def get_voice_endpoint(id_msg:str):
        print(id_msg)
        return FileResponse(f"./ford/voices/{id_msg}.mp3", media_type="audio/mpeg")
    


