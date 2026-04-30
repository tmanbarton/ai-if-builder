from queue import Queue

from backend.agents.agent import generator


def test_generator_yields_messages():
    q = Queue()
    q.put("message 1")
    q.put("message 2")
    q.put(None)

    messages = list(generator(q))
    assert messages == ["message 1", "message 2"]


def test_generator_stops_on_none():
    q = Queue()
    q.put(None)

    messages = list(generator(q))
    assert messages == []