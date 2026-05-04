import json
from pathlib import Path

import numpy as np
from mcp.server.fastmcp import FastMCP
from sentence_transformers import SentenceTransformer

JSON_FILE_PATH = Path(__file__).resolve().parent.parent.parent.parent / "ai-if-builder" / "backend" / "tools" / "embedding" / "embeddings.json"

mcp = FastMCP("if-engine-docs")
sentence_transformer_model = SentenceTransformer("all-MiniLM-L6-v2")

@mcp.tool()
def search_docs(query: str) -> str:
    """
    Search the if-engine's README with natural language input. Uses RAG embedding and returns the top 3 chunks.
    :param query: Natural language question to query the if-engine README.
    :return: Top 3 chunks from cosine similarity based on the embedded query and README.
    """
    with open(JSON_FILE_PATH) as f:
        embeddings_json = json.load(f)

    chunks = [item["text"] for item in embeddings_json]
    embeddings = np.array([item["embedding"] for item in embeddings_json])

    # Embed the input question and compare to embedded README to get closest 3 matches
    input_embedding = sentence_transformer_model.encode(query)
    scores = np.dot(embeddings, input_embedding) / (np.linalg.norm(embeddings, axis=1) * np.linalg.norm(input_embedding))
    top_3 = np.argsort(scores)[-3:]
    # Return top 3 chunks as strings
    return "\n------\n".join(chunks[i] for i in top_3)

if __name__ == "__main__":
    mcp.run()
