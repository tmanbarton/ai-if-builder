My idea: create an app that takes a plan/spec from a user for an interactive
fiction game and turns it into a playable game using a Java library I made: if-engine.

The plan is to use an agentic workflow to do it automatically. User enters their
spec and the LLM goes off and reads my documentation and comes back with a
complete backend for the game.

### Idea for the agent flow:
1. Make the map for the game deterministically. Call Anthropic API for Claude to extract the game map from the spec and return in JSON. I can create Java code deterministically from this.
2. Make another call to Anthropic API again to check for game intro-related stuff. There probably won't be any, but if so, I can deterministically write Java code for that also.
3. Start agentic loop - Claude uses the spec to extract all puzzles in the game into a JSON representation of the puzzles. Including custom commands, if any.
4. Create the custom commands and custom functionality using if-engine based on puzzle JSON and any other custom commands not related to puzzles.
5. Verify commands in code align with puzzles - back to 3 if not (maybe 4? Maybe add a different one?)
6. Verify code compiles and aligns with if-engine - back to 3 if not (maybe 4? Maybe add a different one?)
7. End: Send files to front end to give to user

### Tools/Agents
- **define_puzzles** for extracting puzzles from the spec and into JSON
- **write_commands** for actually writing Java code for the custom commands using the if-engine library
- **verify_puzzles** for checking that the code does what the spec says it should do
- **verify_if_engine** for checking that the code correctly uses the if-engine library. And checks that it compiles in general for any Java related issues

### Also necessary
RAG embedding of the if-engine README and a way for Claude to query the embedded
docs: query_docs.py that uses RAG to query the embedded README. Agents can use that
to get information on the if-engine library.