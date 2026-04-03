from backend.models.game_model import GameModel


def build_map(game_model: GameModel):
    locations = game_model.locations
    connections = game_model.connections
    items = game_model.items
    a = 0

