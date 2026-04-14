# AI Interactive Fiction Builder

A web application that takes a game design spec for an interactive fiction game and uses AI agents to automatically generate Java source files for a playable game, powered by the [if-engine](https://github.com/tmanbarton/if-engine) Java library.

## Features

- **Spec-driven game generation** — describe your game's map, items, puzzles, and commands in plain text, and the system produces Java files
- **Agentic workflow** — Claude-powered agents extract the game map, define puzzles, write custom commands, and verify correctness
- **RAG-based documentation lookup** — agents can query embedded if-engine docs to write correct library usage (planned)
- **Live status streaming** — SSE-based progress updates show agent status in the browser as files are generated

## How It Works

1. User submits a game spec through the web UI
2. The backend calls the Claude API to extract the map (locations, connections, items) into structured JSON
3. Java constants and map-builder code are generated deterministically from the JSON
4. An agentic loop extracts puzzles, writes custom command Java files, and verifies them against the user's spec and the [if-engine](https://github.com/tmanbarton/if-engine) Java library.
5. Generated Java files are returned to the frontend

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
uvicorn backend.endpoint:app --reload
```

Open `http://localhost:8000` in your browser. Paste a game spec into the text area and click **Generate**. Agent status updates will stream in, and generated Java files will appear when complete.

### Game Spec Format

A spec describes the game's locations, map connections, items, commands, and puzzles. See `examples/example1.md` for a full example. Key sections:

- **Locations** — list of named locations
- **Map** — directional connections between locations (e.g. `entrance, north -> kitchen`)
- **Items** — items and their starting locations
- **Custom commands** — new commands the player can use (e.g. `push`)
- **Commands to override** — existing commands with custom behavior (e.g. `take`, `eat`)
- **Puzzles** — multi-step puzzles with success criteria and game state changes

## Project Structure

```
backend/
  endpoint.py          # FastAPI server with /api/generate_files endpoint
  agent.py             # Orchestrates the agentic workflow
  build_map.py         # Extracts map JSON via Claude and generates Java code
  verify_puzzles.py    # Puzzle verification (in progress)
  models/              # Pydantic models for game data (Map, Location, Item, Puzzle, etc.)
  tools/
    definitions.py     # Tool schemas for the Claude agentic loop
    define_puzzles.py  # Puzzle extraction tool
    write_commands.py  # Java command file generation tool
    query_docs.py      # RAG-based if-engine doc lookup (planned)
frontend/
  index.html           # Web UI
  app.js               # Client-side JS for SSE streaming and file display
  styles.css           # Styling
examples/
  example1.md          # Sample game spec ("A Lot at Steak")
  example2.md          # Additional sample spec
tests/
  backend/
    test_build_map.py  # Tests for map building and file generation
    test_agent.py      # Tests for the agent workflow
```

## Tech Stack

- **Backend:** Python, FastAPI, Uvicorn
- **AI:** Anthropic Claude API (structured output + tool use)
- **Frontend:** Vanilla HTML/CSS/JS
- **Testing:** pytest