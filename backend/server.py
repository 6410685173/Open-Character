from fastapi import FastAPI, APIRouter, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from routes import setup_front_ws, setup_chat_route, setup_discord_route
import yaml
import uvicorn



class ServerEngine:

    def __init__(self, configs:dict) -> None:
        self.serverconf:dict = configs["SERVER"]
        self.app:FastAPI = FastAPI()
        self.router:APIRouter = APIRouter()
        self.connections_clients: list[WebSocket] = []
        self._setup_cors_()
        self._setup_routers_()


    def _setup_cors_(self) -> None:
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins="*",
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )


    def _setup_routers_(self) -> None:
        print("Setting up routers...")
        setup_front_ws(self.router, self.connections_clients)
        setup_chat_route(self.router)
        setup_discord_route(self.router)
        self.app.include_router(self.router)
    
    def run(self):
        uvicorn.run(
            app = self.app,
            host = self.serverconf["HOST"],
            port = self.serverconf["PORT"],
            reload = True if self.serverconf["RELOAD"] == "True" else False
        )


if __name__ == "__main__":

    with open('./server_config.yaml', 'r') as file:
        config = yaml.safe_load(file)
        
    # Initialize and start the server
    server = ServerEngine(config)
    server.run()