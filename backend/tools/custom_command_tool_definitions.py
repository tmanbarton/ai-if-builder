from backend.tools.puzzle_tool_definitions import QUERY_DOCS_TOOL
from backend.tools.query_docs import query_docs
from backend.tools.write_custom_commands import write_custom_commands


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