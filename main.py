from fastapi import FastAPI
import uvicorn

from app.config.configs import settings
from app.controller.controller import router


app = FastAPI(title="App")

ip = settings.get("app_host", "localhost")
port = int(settings.get("app_port", 8000))

app.include_router(router)

if __name__ == "__main__": 
    uvicorn.run("main:app", host=ip, port=port)

