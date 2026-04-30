"""
The purpose of this script is to re-embed the if-engine's README when I update it in the if-engine repo.
I run this when I make a change to the README, it updates embeddings.json, and I push the change so the embeddings remain up-to-date.
"""

import json
import re
import urllib.request
from pathlib import Path

from sentence_transformers import SentenceTransformer

from backend.constants import JSON_FILE_PATH, SENTENCE_TRANSFORMER_MODEL

GITHUB_README_URL = "https://raw.githubusercontent.com/tmanbarton/if-engine/main/README.md"

if __name__ == "__main__":
    # Get the README from the public url
    with urllib.request.urlopen(GITHUB_README_URL) as r:
        readme = r.read().decode("utf-8")

    # Split README on markdown headings (#/##/###/####)
    chunks = re.findall("#{1,4}(?:(?!\n#).)*", readme, re.DOTALL)

    model = SentenceTransformer(SENTENCE_TRANSFORMER_MODEL)
    embeddings = model.encode(chunks)

    index = []
    for chunk, embedding in zip(chunks, embeddings):
        index.append({
            "text": chunk,
            "embedding": embedding.tolist(),
        })

    with open(JSON_FILE_PATH, "w") as f:
        json.dump(index, f)
