import queue
from typing import Any

from anthropic import Anthropic

from backend.constants import CLAUDE_SONNET_MODEL
from backend.models.custom_command import CustomCommand
from backend.tools.definitions import CREATE_CUSTOM_COMMANDS_AGENT_TOOLS, CREATE_CUSTOM_COMMAND_TOOL_HANDLERS

agent_system_message = """You are a skilled Java developer and you're only job in life is to write Java code using the if-engine library to create puzzles for an interactive fiction game.
You will receive a pre-parsed JSON object representing custom commands for the interactive fiction game. These commands are available in general game play, i.e. not for specific puzzles.
To get information about the if-engine library, use the query_docs tool. First, analyze the commands and determine what questions need to be asked in order to write the code.
Continue asking questions until you are confident you can write the exact code for the commands and the accompanying logic. Note: the commands can be completely new commands or new, custom logic for exiting default commands.
"""
json_parse_system_message = """You are an expert at extracting important information from user input. Specifically interactive fiction specifications.
Your job is to extract custom commands from a user-provided spec. The spec may or may not specify custom commands. If it does there are two types: completely new commands or overridden default commands.
Your must identify only commands (new or overridden) that apply to the game as a whole, NOT SPECIFIC PUZZLES!
Example 1:
- [user lists locations and items]
- When the player is at the living room location and they "open drawer" or "open coffee table", it reveals a book and picture.
That is a puzzle, don't add an override for the "open" command
Example 2:
- [user lists locations and items]
- The player can say "pray" and the game responds with a funny little prayer message. If they are at the chapel location, the pray message is longer and more meaningful.
- "attend" makes anything that has an action take that action. If a drawer can be opened, "attend" opens it. If a light switch can be switched, "attend" switches it.
- There's one object that can be eaten: potato. When it's eaten, don't do anything besides show a funny message.
"pray" is is an easter egg and can be used anywhere, add this as a custom command with the logic for the chapel.
"attend" can be used anywhere. Add this as a custom command and the logic for automatically taking the action if it's available at the location.
"eat" is a default command, but "eat potato" isn't a puzzle, so add the override and add the simple logic to return a command if it's a potato.
"""

def create_custom_commands(q: queue.Queue, tool_input: dict[str, Any]):
    """
    Sub-agent for writing Java code for custom commands that can be used in the game that aren't puzzle-specific using the if-engine library.
    It has two tools available: query_docs and write_custom_commands. It loops, asking query_docs for info on the library and writing code until it determines it's done.
    :param q: Queue for sending status to SSE connection to show on frontend
    :param tool_input: JSON representing the custom commands to create.
    :return:
    """
    q.put("event: status\ndata: Creating custom commands...\n\n")

    custom_commands: list[CustomCommand] = extract_custom_commands_from_spec(tool_input["user_spec"])

    messages = [{"role": "user", "content": [{"type": "text", "text": custom_commands}]}]
    client = Anthropic()

    # Sub-agent loop
    while True:
        response = client.messages.create(
            model=CLAUDE_SONNET_MODEL,
            max_tokens=16000,
            system=agent_system_message,
            messages=messages,
            tools=CREATE_CUSTOM_COMMANDS_AGENT_TOOLS
        )
        messages.append({"role": "assistant", "content": response.content})

        if response.stop_reason != "tool_use":
            break

        # todo pull out into separate function since this is the same as in agent.run_agent
        tool_results = []
        for block in response.content:
            if block.type == "tool_use":
                # Dispatch the tool using the tool_handler dict
                handler = CREATE_CUSTOM_COMMAND_TOOL_HANDLERS[block.name]
                result = handler(q, block.input)

                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": result
                })

        messages.append({"role": "user", "content": tool_results})

    return response.content[0].text

def extract_custom_commands_from_spec(spec: str):
    messages = [{"role": "user", "content": spec}]
    client = Anthropic()
    response = client.messages.parse(
        model=CLAUDE_SONNET_MODEL,
        max_tokens=16000,
        system=json_parse_system_message,
        messages=messages,
        output_format=list[CustomCommand]
    )

    return response.parsed_output
