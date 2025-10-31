import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import uvicorn
from routers import routers

load_dotenv()

class WebApiApp:
    """
    Singleton class representing the API app.
    Use uvicorn with the instance variables app, port, host and debug.
    """
    
    __DEFAULT_PORT = 8000
    __LOCALHOST = "0.0.0.0"

    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        load_dotenv()

        self.app = FastAPI()
        self.port = int(os.getenv("PORT", self.__DEFAULT_PORT))
        self.host = os.getenv("HOST", self.__LOCALHOST)
        self.debug = os.getenv("DEBUG", False).lower() == "true"

        self.__add_middlewares()
        self.__add_routers(routers)
        
        self._initialized = True
    
    def __add_routers(self, routers):
        for router in routers:
            self.app.include_router(router)

    def __add_middlewares(self):
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"]
        )
        

web_api_app = WebApiApp()
app = web_api_app.app

if __name__ == "__main__":
    uvicorn.run(
        "app:app", 
        host=web_api_app.host, 
        port=web_api_app.port, 
        reload=web_api_app.debug
    )