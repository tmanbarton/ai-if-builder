from backend.agents.create_puzzles_agent import create_puzzles
from backend.agents.create_custom_commands_agent import create_custom_commands
from backend.tools.query_docs import query_docs

TOOL_HANDLERS = {
    "create_puzzles": create_puzzles,
    "create_custom_commands": create_custom_commands,
    "query_docs": query_docs,
}

TOOL_DEFINITIONS = [
    {
        "name": "create_custom_commands",
        "description": """This tool is for writing a Java file or files to create custom interactive fiction commands using the if-engine Java
library. Use this tool if no custom commands have been created and when you have the JSON representation of the game's
puzzles (which contain the custom commands).""",
        "input_schema": {
           "type": "object",
           "properties": {
                "user_spec": {
                    "type": "string",
                    "description": "This is the specification that the user provided as an input. The tool will use this to parse out the commands into JSON then write code.",
                }
            },
           "required": ["user_spec"],
       }
    },
    {
        "name": "create_puzzles",
        "description": """This tool is for writing Java code for puzzles defined in a user-defined specification.
Use this tool after custom commands have been created or intentionally skipped. This tool analyzes the spec tp identify then parse out the puzzles
into JSON to ultimately write the code for functional puzzles.
""",
        "input_schema": {
            "type": "object",
            "properties": {
                "user_spec": {
                    "type": "string",
                    "description": "This is the specification that the user provided as an input. The tool will use this to parse out the puzzles into JSON then write code.",
                }
            },
            "required": ["user_spec"],
        }
    }
]
