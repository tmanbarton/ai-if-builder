import queue

def generator(q: queue.Queue):
    while True:
        message: str = q.get()
        if message is None:
            return
        yield message

def run_agent(q: queue.Queue, spec: str):
    q.put("event: status\ndata: Starting\n\n")