# todo copy over RAG for if-engine documentation from other project
import queue

system_message = """
Use this tool whenever you need information about how to use the if-engine Java library.
This tool allows you to queries the if-engine repo's README using natural language, so ask anything about implementation details for parts of 
the game that can't be implemented deterministically. An example would be a custom command. Use this tool to determine how a custom command is built.
You will receive a JSON blob with fields that include a description of what the particular object should do.
Your job is to identify what code is needed to create the part of the game in question.
Example: puzzle with description: Player must use the key to unlock and open a door to reveal hidden items: jar, hammer, and hatchet.
You have several questions to ask. "How do I make something unlock using this library?" "How do I reveal hidden items using this library?"
Repeat this until you have a complete understanding of how to create the puzzle.
Note: Commands can be completely custom or can override existing commands, based on the exact command provided, you must determine what is the
relevant questions to ask. 
"""

def query_docs(q: queue.Queue, spec: str):
    a = 0