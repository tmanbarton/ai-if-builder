from backend.tools.query_docs import query_docs
from backend.tools.write_puzzles import write_puzzles


CREATE_PUZZLES_TOOL_HANDLERS = {
    "query_docs": query_docs,
    "write_puzzles": write_puzzles
}

# Create as separate variable so custom_command_tool_definitions can use it since it's the same tool.
QUERY_DOCS_TOOL = {
    "name": "query_docs",
    "description": """Use this tool whenever you need information about how to use the if-engine Java library.
This tool allows you to queries the if-engine repo's README using natural language, so ask anything about implementation details for parts of the game that can't be implemented deterministically. An example would be a custom command. Use this tool to determine how a custom command is built.
You will receive a JSON blob with fields that include a description of what the particular object should do. Your job is to identify what code is needed to create the part of the game in question.
Example: puzzle with description: Player must use the key to unlock and open a door to reveal hidden items: jar, hammer, and hatchet.
You have several questions to ask. "How do I make something unlock using this library?" "How do I reveal hidden items using this library?"
Repeat this until you have a complete understanding of how to create the puzzle.
Note: Commands can be completely custom or can override existing commands, based on the exact command provided, you must determine what is the relevant questions to ask.""",
    "input_schema": {
        "type": "object",
        "properties": {
            "question": {
                "type": "string",
                "description": "The question to query the if-engine documentation about."
            }
        },
        "required": ["question"]
    }
}

CREATE_PUZZLES_AGENT_TOOLS = [
    QUERY_DOCS_TOOL,
    {
        "name": "write_puzzles",
        "description": "This tool is for writing Java code for the puzzles using the if-engine Java library. At this point you have learned how to use the if-engine library "
                       "and know exactly what to do. Now you need to write the code. You will tell this tool what code you want to write and it "
                       "will write it to a local file.",
        "input_schema": {
            "type": "object",
            "properties": {
                "files": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "file_name": {
                                "type": "string",
                                "description": "The name of the file you are going to write to. It should end in .java"
                            },
                            "code": {
                                "type": "string",
                                "description": "This is the exact code that will be written to the Java file. It will either be a new file or appended to an existing file."
                            },
                            "is_new_file": {
                                "type": "boolean",
                                "description": "Whether or not this a new file or not. True if it's a new file, false otherwise. "
                                               "This is to determine if the code should be appended to an existing file or if a new file should be created."
                            }
                        },
                        "required": ["file_name", "code", "is_new_file"]
                    },
                }
            },
            "required": ["files"],
        }
    }
]