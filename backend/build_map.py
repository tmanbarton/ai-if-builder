import queue

from anthropic import Anthropic

from backend.models.game_model import GameModel
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
    messages = [{"role": "user", "content": spec}]

    q.put("event: status\ndata: Building map\n\n")
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

    for item in items:
        print(f"""\
.placeItem(new Item(
  "{item.name}",
  "{item.inventory_description}",
  "{item.location_description}",
  "{item.detailed_description}",
  Set.of({", ".join(f'"{a}"' for a in item.aliases)}),
  "{item.location}"
)\
""")

    for location in locations:
        print(f"""\
.addLocation(new Location(
  "{location.name}",
  "{location.long_description}"
  "{location.short_description}",
)\
""")
        if location.is_starting_location:
            print(f'.setStartingLocation("{location.name}")')

    for connection in connections:
        print(f'.connectOneWay("{connection.source_location}", Direction.{connection.direction}, "{connection.target_location}")')
    a = 0
