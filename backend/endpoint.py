from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

app = FastAPI()

class Request(BaseModel):
    game_spec: str

def some_generator():
    yield "event: status1\ndata: data1\n\n"
    yield "event: status2\ndata: data2\n\n"

@app.post("/agent/some_endpoint")
def some_endpoint(request: Request):
    return StreamingResponse(some_generator(), media_type="text/event-stream")