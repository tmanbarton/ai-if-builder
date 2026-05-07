from backend.tools.puzzle_tool_definitions import SEARCH_DOCS_TOOL
from backend.tools.search_docs import search_docs
from backend.tools.write_custom_commands import write_custom_commands


CREATE_CUSTOM_COMMAND_TOOL_HANDLERS = {
    "search_docs": search_docs,
    "write_custom_commands": write_custom_commands
}
CREATE_CUSTOM_COMMANDS_AGENT_TOOLS = [
    SEARCH_DOCS_TOOL,
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
                            "db_operation_type": {
                                "type": "string",
                                "description": """You have three options: 'INSERT', 'UPDATE', or 'APPEND'. You must choose ONLY ONE of those options and NO OTHER VALUES.
Insert means you have a new file you want to create. Update means you want to replace an existing file with a new version.
Append means you want to add some more content on the end of an existing file.
Append is uncommon since you would need to replace the brackets at the end of the Java file.
Make sure if you are updating a file you know you won't break anything by accidentally deleting old functionality."""
                            }
                        },
                        "required": ["file_name", "code", "db_operation_type"]
                    },
                }
            },
            "required": ["files"],
        }
    }
]