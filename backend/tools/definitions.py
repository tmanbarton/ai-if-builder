from backend.agents.create_puzzles_agent import create_puzzles
from backend.agents.create_custom_commands import create_custom_commands
from backend.tools.query_docs import query_docs
from backend.tools.write_custom_commands import write_custom_commands
from backend.tools.write_puzzles import write_puzzles

TOP_LEVEL_TOOL_HANDLERS = {
    "create_puzzles": create_puzzles,
    "create_custom_commands": create_custom_commands,
    "query_docs": query_docs,
}

TOP_LEVEL_TOOL_DEFINITIONS = [
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

CREATE_PUZZLES_TOOL_HANDLERS = {
    "query_docs": query_docs,
    "write_puzzles": write_puzzles
}

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

CREATE_CUSTOM_COMMAND_TOOL_HANDLERS = {
    "query_docs": query_docs,
    "write_custom_commands": write_custom_commands
}
CREATE_CUSTOM_COMMANDS_AGENT_TOOLS = [
    QUERY_DOCS_TOOL,
    {
        "name": "write_custom_commands",
        "description": "This tool is for writing Java code for custom commands using the if-engine Java library. At this point you have learned how to use the if-engine library "
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