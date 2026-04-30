from pathlib import Path

JSON_FILE_PATH = Path(__file__).resolve().parent.parent.parent.parent / "backend" / "tools" / "embedding" / "embeddings.json"
SENTENCE_TRANSFORMER_MODEL = "all-MiniLM-L6-v2"
CLAUDE_SONNET_MODEL = "claude-sonnet-4-6"
CLAUDE_HAIKU_MODEL = "claude-haiku-4-5"