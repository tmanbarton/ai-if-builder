from backend.tools.create_puzzles import create_puzzles
from backend.tools.create_custom_commands import create_custom_commands
from backend.tools.query_docs import query_docs

TOOL_HANDLERS = {
   "create_puzzles": create_puzzles,
   "create_custom_commands": create_custom_commands,
   "query_docs": query_docs,
}

TOOL_DEFINITIONS = [
    {
       "name": "create_puzzles",
       "description": "This tool is for writing puzzles using the if-engine Java library based on descriptions of the puzzles and custom command"
                      "logic. Use this tool when you if you haven't created any puzzles yet.",
       "input_schema": {
           "type": "object",
           "properties": {
               "puzzles": {
                   "type": "array",
                   "description": "This is an array of all the puzzles in the game. A puzzle is anything the user must do in order to progress the"
                                  "game other than move from location to location. The input spec may have any number of puzzles and the user"
                                  "may indicate them explicitly or implicitly. Examples of explicit puzzles: \n'Puzzles: \n- The player needs to open"
                                  "a drawer to reveal a key.\n- The player uses the key to unlock a door in the basement.' Examples or implicit"
                                  "puzzles: 'The player starts in the kitchen. They need to find a key in the drawer by opening it then use that"
                                  "key to open a drawer in the basement.'",
                   "items": {
                       "type": "object",
                       "properties": {
                           "custom_command_logic": {
                               "type": "array",
                               "items": {
                                   "type": "string",
                                   "description": "This is the exact string of the command that the user would type to initiate the custom logic."
                                           "e.g. 'push' or 'take'. This includes completely new commands and overridden commands."
                                },
                               "description": "List of all custom commands that this puzzle requires. This includes completely new commands and"
                                              "overridden commands."
                            },
                           "detailed_description": {
                               "type": "string",
                               "description": "This is the detailed descriptions of the puzzle. The description should include the"
                                              "setup (if necessary), the success criteria, detailed information on how the puzzle works,"
                                              "commands that are needed and details on corner cases and happy paths. Example: 'The user needs to"
                                              "find 3 numbers that unlock a vault. The numbers are scattered around various locations - pantry (4),"
                                              "grocery store (23), and cafeteria (87). There's a notebook found at the desk that indicates the"
                                              "order of the numbers (87, 4, 23) which unlocks the vault. When the player gets those numbers and is"
                                              "at the vault location they can use the 'enter' command with the numbers with 'enter 87 4 23' to"
                                              "unlock the vault or use the default 'unlock'. You must specify how custom command logic works,"
                                              "whether that's new commands or overridden commands."
                            }
                        },
                       "required": ["custom_command_logic", "detailed_description"],
                    }
                }
            },
           "required": ["puzzles"],
        }
    },
    {
       "name": "create_custom_commands",
       "description": "This tool is for writing a Java file or files to create custom interactive fiction commands using the if-engine Java"
                      "library. Use this tool if no custom commands have been created and when you have the JSON representation of the game's"
                      "puzzles (which contain the custom commands).",
       "input_schema": {
           "type": "object",
           "properties": {
               "commands": {
                   "type": "array",
                   "items": {
                       "type": "object",
                       "properties": {
                           "command_name": {
                               "type": "string",
                               "description": "This is the exact string of the command that the user would type to initiate the custom logic. e.g."
                                              "'push' or 'take'"
                            },
                           "command_description": {
                               "type": "string",
                               "description": "This is the description of what the custom command does and how it works in as much detail as"
                                              "possible. If this is a completely new command, consider various states for when/how the user could"
                                              "use the command (example: 'eat [object]' or just 'eat', and the object could be in the inventory, or"
                                              "at the location, or not present at all). If this is an overridden command, only the specific/custom"
                                              "use case needs to be handled, other use cases would fall through to the default behavior."
                                              "Note this DOES NOT include commands that are only applicable for specific puzzles. These commands"
                                              "are ones that are generally applicable throughout the game, outside of puzzles (though they can be"
                                              "Easter egg-like where they only apply in a certain scenario, if applicable)."
                            }
                        },
                       "required": ["command_name", "command_description"],
                    }
                }
            },
           "required": ["commands"],
        }
    },
    {
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
]