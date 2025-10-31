import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import uvicorn
from routers import routers

__DEFAULT_PORT = 8000
__LOCALHOST = "0.0.0.0"

load_dotenv()

app = FastAPI()
port = int(os.getenv("PORT", __DEFAULT_PORT))
host = os.getenv("HOST", __LOCALHOST)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"]
    
)

for router in routers:
    app.include_router(router)
    
if __name__ == "__main__":
    uvicorn.run("app:app", host=host, port=port, reload=True)