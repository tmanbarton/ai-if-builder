# AI Interactive Fiction Builder

A web application that takes a game design spec for an interactive fiction game and uses AI agents to automatically generate Java source files for a playable game, powered by the [if-engine](https://github.com/tmanbarton/if-engine) Java library.

## Features

- **Spec-driven game generation** — describe your game's map, items, puzzles, and commands in plain text, and the system produces Java files
- **Agentic workflow** — Claude-powered agents extract the game map, define puzzles, write custom commands, and verify correctness
- **RAG-based documentation lookup** — agents can query embedded if-engine docs via an MCP server to write correct library usage
- **Live status streaming** — SSE-based progress updates show agent status in the browser as files are generated
- **Zip download** — download all generated files as a ready-to-build Gradle project

## How It Works

1. User submits a game spec through the web UI
2. The backend generates scaffolding files (build.gradle, App.java, Game.java, GameWebSocketServer.java)
3. The Claude API extracts the map (locations, connections, items) into structured JSON
4. Java constants and map-builder code are generated deterministically from the JSON
5. Sub-agents handle puzzles and custom commands via tool use
6. Generated files are streamed to the frontend and stored in SQLite for download
7. User clicks **Download .zip** to get a complete Gradle project

## Installation

**Prerequisites:** Python 3.10+, an [Anthropic API key](https://console.anthropic.com/)

```bash
# Clone the repository
git clone <repo-url>
cd ai-if-builder

# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install fastapi uvicorn anthropic pydantic

# Set your API key
export ANTHROPIC_API_KEY="your-key-here"
```

## Usage

Start the server:

```bash
uvicorn backend.endpoints.generate_code_endpoint:app --reload
```

Open `http://localhost:8000` in your browser. Paste a game spec into the text area and click **Generate**. Agent status updates will stream in, and generated Java files will appear when complete. Click **Download .zip** to get the full Gradle project.

### Game Spec

A spec describes your game's map, items, commands (if any), and puzzles (if any). See `examples/example1.md` for an example.

## Project Structure

```
backend/
  endpoints/
    generate_code_endpoint.py  # FastAPI app, POST /api/generate_code
    download_zip_endpoint.py   # GET /api/download_zip/{session_id}
  agents/
    agent.py                   # Main agentic loop orchestrator
    create_puzzles_agent.py    # Puzzle creation sub-agent
    create_custom_commands_agent.py  # Custom command sub-agent
  models/                      # Pydantic models (Map, Location, Item, Puzzle, etc.)
  tools/
    definitions.py             # Tool schemas and handler registry
    write_puzzles.py           # Puzzle file generation tool
    write_custom_commands.py   # Custom command file generation tool
    search_docs.py             # RAG-based if-engine doc lookup
    embedding/                 # Embedding utilities for doc search
  mcp_server/
    search_docs_server.py      # MCP server for documentation queries
  build_map.py                 # Extracts map JSON via Claude, generates Java code
  create_intro.py              # Intro/opening sequence generation
  game_scaffolding.py          # Boilerplate Java and frontend files
  database.py                  # SQLite operations for generated file storage
  db_helpers.py                # Insert/upsert/append helpers
  verify_puzzles.py            # Puzzle verification logic
frontend/
  index.html                   # Web UI
  app.js                       # SSE streaming, file display, download button
  styles.css                   # Styling
examples/
  example1.md                  # Sample game spec ("A Lot at Steak")
  example2.md                  # Additional sample spec
tests/
  backend/
    test_build_map.py          # Map building and file generation tests
    test_agent.py              # Agent workflow tests
    test_database.py           # Database operation tests
    test_create_intro.py       # Intro creation tests
```

## Tech Stack

- **Backend:** Python, FastAPI, Uvicorn, SQLite
- **AI:** Anthropic Claude API (structured output + tool use)
- **Frontend:** Vanilla HTML/CSS/JS
- **Testing:** pytest