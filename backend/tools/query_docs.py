import json
import queue
from typing import Any

import numpy as np
from anthropic import Anthropic
from sentence_transformers import SentenceTransformer

from backend.constants import JSON_FILE_PATH, SENTENCE_TRANSFORMER_MODEL, CLAUDE_HAIKU_MODEL

system_message = """
You will be provided with a question and the top 3 chunks from RAG embedding of the README for the if-engine repo.
Provide an answer to the question based on the given documentation.
You must provide code examples when necessary. **Accuracy** is **important**. Be precise with your wording with no room for ambiguity.
If something is unclear in the question, ask for clarification. If the docs don't answer the question, say so.
"""
# todo add a little more at the end for if the docs don't answer the question?
model = SentenceTransformer(SENTENCE_TRANSFORMER_MODEL)

def query_docs(q: queue.Queue, tool_input: dict[str, Any]):
    q.put("event: status\ndata: Fetching documentation...\n\n")
    return query_embedding(tool_input["question"])

def query_embedding(query: str):
    with open(JSON_FILE_PATH) as f:
        embeddings_json = json.load(f)

    chunks = [item["text"] for item in embeddings_json]
    embeddings = np.array([item["embedding"] for item in embeddings_json])

    # Embed the input question and compare to embedded README to get closest 3 matches
    input_embedding = model.encode(query)
    scores = np.dot(embeddings, input_embedding) / (np.linalg.norm(embeddings, axis=1) * np.linalg.norm(input_embedding))
    top_3 = np.argsort(scores)[-3:]

    # Prepare user message to send to LLM - contains input and the documentation found
    context = "\n\n".join(chunks[i] for i in top_3)
    augmented_input = f"Question:\n{query}\n\nDocumentation:\n{context}"
    messages = [{"role": "user", "content": augmented_input}]

    # Send to LLM
    client = Anthropic()
    response = client.messages.create(
        model=CLAUDE_HAIKU_MODEL,
        max_tokens=16000,
        system=system_message,
        messages=messages
    )

    return response.content[0].text
