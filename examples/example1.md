This game is called "A Lot at Steak". The player is a mouse at a steak house and the goal of the game is to get to the
steak in the kitchen.

### Locations:
- Entrance
- Waiting area
- Host stand
- Tables
- Aisle
- More tables
- Even more tables
- Bar
- Lounge
- More tables in the back
- Restrooms
- Kitchen
- Back of kitchen

### Map
- Entrance, west -> waiting area
- Entrance, north -> host stand
- Waiting area, east -> entrance
- Waiting area, northeast -> host stand
- host stand, south -> entrance
- host stand, southwest -> waiting area
- host stand, north -> tables
- tables, south -> host stand
- tables, west -> more tables
- tables, north -> aisle
- more tables, north -> even more tables
- aisle, south -> tables
- aisle, north -> aisle continued
- aisle continued, west -> even more tables
- aisle continued, east -> lounge
- aisle continued, north -> kitchen
- lounge, west -> aisle continued
- kitchen, south -> aisle continued
- kitchen, north -> back of kitchen
- back of kitchen, south -> kitchen

### Items:
- Peanuts - waiting area
- Fork - tables
- Knife - more tables
- Menu - host stand

### Commands to override:
- *"take"* : A mouse can't really pick up things - especially the items available in the game - so this isn't an option. The game will just respond with "A mouse can't pick that up."
- *"climb"* : Mouse can actually "climb" a table at the "more tables" location and it results in some game state change - the mouse is on the table.
- *"eat"* : The mouse can eat the peanuts and the steak at the end.

### Custom commands:
- *"push"* : A mouse can push things around. e.g. "push knife" or "push menu".
  - Don't fall through to the default behavior. This should have a custom default behavior.

### Puzzles:
- Knife
  - Mouse climbs onto the table with a knife on it at the "more tables" location.
  - Mouse pushes the knife off and it falls onto the foot of a passing server.
  - Server runs/limps into the kitchen screaming about a mouse stabbing his foot
  - Mouse jumps down from table to avoid notice
  - Creates chaos and an opportunity to get into the kitchen since there are a bunch of people going in and out now
  - Adds something about "severs running about" to the end of each location description.
- Broom
  - Broom in the kitchen that looks like it could work as a ramp if it was knocked over
  - Mouse can "push" the broom over to make it into a ramp that the mouse can climb up and onto the counter to get to the steak