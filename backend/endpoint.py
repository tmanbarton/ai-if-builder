import threading
from queue import Queue

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from backend.agent import run_agent, generator

app = FastAPI()

class Request(BaseModel):
    game_spec: str

@app.post("/agent/generate_files")
def generate_files(request: Request):
    q = Queue()
    thread = threading.Thread(target=run_agent, args=(q, request))
    thread.start()
    return StreamingResponse(generator(q), media_type="text/event-stream")