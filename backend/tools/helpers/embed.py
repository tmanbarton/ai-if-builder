"""
The purpose of this script is to re-embed the if-engine's README when I update it in the if-engine repo.
I run this when I make a change to the README, it updates embeddings.json, and I push the change so the embeddings remain up-to-date.
"""

import json
import re
import urllib.request
from pathlib import Path

from sentence_transformers import SentenceTransformer

GITHUB_README_URL = "https://raw.githubusercontent.com/tmanbarton/if-engine/main/README.md"
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
JSON_FILE_PATH = PROJECT_ROOT / 'backend' / 'tools' / 'helpers' / 'embeddings.json'

# Get the README from the public url
with urllib.request.urlopen(GITHUB_README_URL) as r:
    readme = r.read().decode("utf-8")

# Split README on markdown headings (#/##/###/####)
chunks = re.findall("#{1,4}(?:(?!\n#).)*", readme, re.DOTALL)

model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = model.encode(chunks)

index = []
for chunk, embedding in zip(chunks, embeddings):
    index.append({
        "text": chunk,
        "embedding": embedding.tolist(),
    })

with open(JSON_FILE_PATH, "w") as f:
    json.dump(index, f)
