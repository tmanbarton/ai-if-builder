import os
import threading

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from queue import Queue

from backend.agent import run_agent, generator
from backend.database import init_db

app = FastAPI()
init_db()

class Request(BaseModel):
    game_spec: str

@app.post("/api/generate_files")
def generate_files(request: Request):
    q = Queue()
    thread = threading.Thread(target=run_agent, args=(q, request.game_spec))
    thread.start()
    return StreamingResponse(generator(q), media_type="text/event-stream")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
app.mount("/", StaticFiles(directory=os.path.join(BASE_DIR, "frontend"), html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("endpoint:app", reload=True)