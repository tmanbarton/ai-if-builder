TOOL_DEFINITIONS = [
    {
        'name': 'define_puzzles',
        'description': "This tool is for extracting puzzles from the user's input spec for the interactive fiction game. Use this as the first "
                       "tool call. If no other tools have been called and if you don't have the puzzle JSON, use this tool. Other tools depend on "
                       "the puzzles to be parsed.",
        'input_schema': {
            'type': 'object',
            'properties': {
                'puzzles': {
                    'type': 'array',
                    'description': 'This is an array of all the puzzles in the game. A puzzle is anything the user must do in order to progress the '
                                   'game other than move from location to location. The input spec may have any number of puzzles and the user '
                                   'may indicate them explicitly or implicitly. Examples of explicit puzzles:\n"Puzzles:\n- The player needs to open '
                                   'a drawer to reveal a key.\n- The player uses the key to unlock a door in the basement." Examples or implicit '
                                   'puzzles: "The player starts in the kitchen. They need to find a key in the drawer by opening it then use that '
                                   'key to open a drawer in the basement."',
                    'items': {
                        'type': 'object',
                        'properties': {
                            'custom_commands': {
                                'type': 'array',
                                'items': {
                                    'type': 'string',
                                    'description': 'This is the exact string of the command that the user would type to initiate the custom logic. '
                                            'e.g. "push" or "take"'
                                },
                                'description': 'List of all custom commands that this puzzle requires. This includes completely new commands and '
                                               'overridden commands.'
                            },
                            'detailed_description': {
                                'type': 'string',
                                'description': 'This is the detailed descriptions of the puzzle. The description should include the '
                                               'setup (if necessary), the success criteria, detailed information on how the puzzle works, '
                                               'commands that are needed and details on corner cases and happy paths. Example: "The user needs to '
                                               'find 3 numbers that unlock a vault. The numbers are scattered around various locations - pantry (4), '
                                               'grocery store (23), and cafeteria (87). There\'s a notebook found at the desk that indicates the '
                                               'order of the numbers (87, 4, 23) which unlocks the vault. When the player gets those numbers and is '
                                               'at the vault location they can use the \'enter\' command with the numbers with \'enter 87 4 23\' to '
                                               'unlock the vault."'
                            }
                        },
                        'required': ['custom_commands', 'detailed_description'],
                    }
                }
            },
            'required': ['puzzles'],
        }
    },
    {# todo consider if this should be writing one command at a time or all commands.
     #  Might need to restructure if it's all commands, and might need to rename if it's only one command
        "name": "write_commands",
        "description": 'This tool is for writing a Java file or files to create custom interactive fiction commands using the '
                       'if-engine Java library. You will receive a JSON representation of a game\'s puzzles, and the custom commands they require.'
                       'You will receive the input spec and decide if there are custom commands needed. If so, use this tool first. '
                       'Ways to determine there are custom commands: the user explicitly mentions a custom command, a custom command is mentioned in '
                       'a puzzle. Custom commands can either be completely new commands (e.g. "blow", "sweep"), or they can be overriding '
                       'existing commands (e.g. "look", "eat"). Your job is to identify the name and describe in detail what the custom command '
                       'is supposed to do.',
        "input_schema": {
            "type": "object",
            "properties": {
                "command_name": {
                    "type": "string",
                    "description": 'This is the exact string of the command that the user would type to initiate the cusotm logic. e.g. "push" or "take"'
                },
                "command_description": {
                    "type": "string",
                    "description": "This is the description of what the custom command does and how it works in as much detail as possible. "
                                   "If this is a completely new command, consider various states for when/how the user could use the command "
                                   "(example: 'eat [object]' or just 'eat', and the object could be in the inventory, or at the location, "
                                   "or not present at all). If this is an overridden command, only the specific/custom use case needs to be handled, "
                                   "other use cases would fall through to the default behavior."
                }
            },
            "required": ["command_name", "command_description"],
        }
    }
]