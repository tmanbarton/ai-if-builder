TOOL_DEFINITIONS = [
    {
        "name": "create_commands",
        "description": "",
        "input_schema": {
            "type": "object",
            "properties": {
                "command_name": {
                    "type": "string",
                    "description": 'This is the exact string of the command that the user would type to initiate the cusotm logic. e.g. "push" or "take"'
                },
                "command_description": {
                    "type": "string",
                    "description": "This is the description of what the custom command does and how it works in as much detail as possisble. "
                }
            },
            "required": ["command_name"]
        }
    }
]