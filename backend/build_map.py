import os
import queue

from anthropic import Anthropic

from backend.models.connection import Connection
from pathlib import Path
from backend.models.item import Item
from backend.models.location import Location
from backend.models.map import Map

system_message = """
Your only job in life is to extract an interactive fiction map from a spec input into JSON.
The user will provide some sort of text representation of the map (directed graph data structure) and they may or may not provide a separate list of locations alone. If they don't provide a list of locations, you must determine all locations based on the map they provide.
A common format for representing this is: `location1 north -> location2`, `location2 south -> location1`
This would indicate location1 leads north to location2 and location2 leads south to location1.
Note, the user may use a different format, but use your best judgement to determine what the user intends the structure to be.
They will also provide items and indicate what locations those items are at.
There are several fields for you to populate as described in the structured output fields for locations and items.
Note: DO NOT try to fill in the descriptions with actual text, use placeholder text like "cave long description" or "backpack detailed description". The user will complete the full descriptions themselves.
"""


def build_map(q: queue.Queue, spec: str):
    """
    Sends the spec input to Claude and parses the JSON response representing the map to create the game map code.
    This includes the locations and their connections, and the items. Those are the only aspects that can
    be created deterministically from the JSON.
    :param q: Queue for sending SSE events to the front end. Automatically sends the message when an element is added
    :param spec: Game spec that the user submitted to send to Claude.
    """
    q.put("event: status\ndata: Building map...\n\n")

    messages = [{"role": "user", "content": spec}]
    client = Anthropic()
    response = client.messages.parse(
        model="claude-sonnet-4-6",
        max_tokens=16000,
        system=system_message,
        messages=messages,
        output_format=Map
    )
    game_map: Map = response.parsed_output

    locations = game_map.locations
    connections = game_map.connections
    items = game_map.items
    write_files(locations, connections, items)
    q.put("event: status\ndata: Map created...\n\n")


def write_files(locations: list[Location], connections: list[Connection], items: list[Item],
                output_root_dir: str = Path(__file__).parent.parent):
    os.makedirs(f"{output_root_dir}/generated_files", exist_ok=True)
    # Create constants for items and locations. Use the item/location name in all caps for variable names
    with open(f"{output_root_dir}/Constants.java", "w") as f:
        f.write("///// Item constants /////")
        for item in items:
            screaming_snake_case_name = item.name.upper().replace(" ", "_")
            f.write(f"""
public static final String {screaming_snake_case_name}_NAME = "{item.name}";
public static final String {screaming_snake_case_name}_INVENTORY_DESCRIPTION = "{item.inventory_description}";
public static final String {screaming_snake_case_name}_LOCATION_DESCRIPTION = "{item.location_description}";
public static final String {screaming_snake_case_name}_DETAILED_DESCRIPTION = "{item.detailed_description}";
public static final Set<String> {screaming_snake_case_name}_ALIASES = Set.of({", ".join(f'"{a}"' for a in item.aliases)});
            """)

        f.write("\n///// Location constants /////")
        for location in locations:
            screaming_snake_case_name = location.name.upper().replace(" ", "_")
            f.write(f"""
public static final String {screaming_snake_case_name}_NAME = "{location.name}";
public static final String {screaming_snake_case_name}_SHORT_DESCRIPTION = "{location.short_description}";
public static final String {screaming_snake_case_name}_LONG_DESCRIPTION = "{location.long_description}";
            """)

    # Create the map items and connections using the Java if-engine library's builder.
    # Write to a .txt file to pass to Claude later so it can add it to the rest of the game
    with open(f"{output_root_dir}/map.txt", "w") as f:

        f.write("///// Add Items /////")
        # Parameters: placeItem(new Item(name, inventory description, location description, detailed description, aliases), targetLocation)
        for item in items:
            screaming_snake_case_name = item.name.upper().replace(" ", "_")
            f.write(f"""
.placeItem(new Item(
  Constants.{screaming_snake_case_name}_NAME,
  Constants.{screaming_snake_case_name}_INVENTORY_DESCRIPTION,
  Constants.{screaming_snake_case_name}_LOCATION_DESCRIPTION,
  Constants.{screaming_snake_case_name}_DETAILED_DESCRIPTION,
  Constants.{screaming_snake_case_name}_ALIASES),
  Constants.{item.location.upper().replace(" ", "_")}_NAME))""")

        f.write("\n\n///// Add Locations /////")
        # Parameters: .addLocation(new Location(name, long description, short description))
        for location in locations:
            screaming_snake_case_name = location.name.upper().replace(" ", "_")
            f.write(f"""
.addLocation(new Location(
  Constants.{screaming_snake_case_name}_NAME,
  Constants.{screaming_snake_case_name}_LONG_DESCRIPTION,
  Constants.{screaming_snake_case_name}_SHORT_DESCRIPTION))""")
            if location.is_starting_location:
                f.write(f"\n.setStartingLocation(Constants.{screaming_snake_case_name}_NAME)")

        f.write("\n\n///// Connect Locations /////\n")
        # Parameters: .connectOneWay(source location name, direction, target location name)
        for connection in connections:
            f.write(
                f'.connectOneWay(Constants.{connection.source_location.upper().replace(" ", "_")}_NAME, Direction.{connection.direction}, '
                f'Constants.{connection.target_location.upper().replace(" ", "_")}_NAME)\n')
