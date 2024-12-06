from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from ford.AIEngine import AICharacter
import yaml
import json



# for connecting between frontend-backend
def setup_front_ws(router:APIRouter, connected_clients:list[WebSocket]):

    with open('./engine_config.yaml', 'r', encoding='utf-8') as file:
        config = yaml.safe_load(file)
        
        
    @router.websocket("/front_ws")
    async def frontend_websocket_endpoint(websocket: WebSocket):
        await websocket.accept()
        connected_clients.append(websocket)
        id_memory = await websocket.receive()
        print(id_memory)
        ford = AICharacter(id=json.loads(id_memory["text"]).get("id"), configs=config)
        
        try:
            while True:

                data = await websocket.receive()
                print(f'front-end data: {data}')
                # Determine if the message is text or binary (audio)
                if isinstance(data, dict):  # Assuming it's JSON (for text data)
                    try:
                        # Handle text message
                        data_object = json.loads(data["text"])

                        if data_object.get("action") == "fetch_history":
                            response = {
                                "history": ford.get_memory()  # Include the list of messages in 'history' field
                            }
                            await websocket.send_text(json.dumps(response))
                        elif data_object.get("action") == "get_voice":
                            voice = ford.get_voice(id=data_object.get("id"))
                            
                            await websocket.send_bytes(voice)

                        else:
                            try:
                                response = ford.thinking(data_object["message"], data_object["stream"])
                                
                                text = ""
                                if hasattr(response, '__iter__') and not isinstance(response, dict): # stream
                                    for partial_response in response:
                                        await websocket.send_text(partial_response)
                                        text+= partial_response
                                        print(partial_response, end="")
                                    voice = ford.speak(text, stream=True)
                                    await websocket.send_bytes(voice)

                                else:
                                   
                                    await websocket.send_text(json.dumps(response))
                                    text+= response["content"]
                                    
                                    voice = ford.speak(text, stream=False, id=response["id"])
                                    await websocket.send_bytes(voice)
                            except Exception as e:
                                print(e)


                    except json.JSONDecodeError:
                        print("Failed to decode message as JSON")
     



                elif isinstance(data, bytes):  # Assuming it's binary (for audio data)
                    
                    audio_data = data
                    text = ford.listen(audio_data)
                    sentence = ""
                    for partial_response in ford.thinking(text):
                        await websocket.send_text(partial_response)
                        # Optionally log each chunk to the console
                        print(partial_response, end="")
                        sentence += partial_response
                    ford.speak(sentence, False)

                
        except WebSocketDisconnect:
            # Remove the client from the connected clients list on disconnect
            connected_clients.remove(websocket)