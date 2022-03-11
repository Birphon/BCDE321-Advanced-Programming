class Player:
    def __init__(self, name, health=6, attack_score=1, items=[], current_tile=None, previous_tile=None,
                 has_totem=False):
        self.name = name
        self.hp = health
        self.attack_score = attack_score
        self.items = items
        self.current_tile = current_tile
        self.previous_tile = previous_tile
        self.has_totem = has_totem

    def hold_totem(self):
        if Player.__init__(has_totem=True):
            return "You are holding the Totem. Find the Graveyard before time runs out"


class Tile:
    pass


class TileType:
    def indoor(self):
        return "This is an indoor tile"

    def outdoor(self):
        return "This is an outdoor tile"


class DevelopmentCard:
    pass


class Items:
    pass


class GameConditions: # Win / Loss conditions
    pass


class Action:
    pass


class GameStart:
    pass


class Garden:
    def name(self):
        name = "Garden"
        effect = "Health +1 if End Turn here"
        tile_type = TileType.outdoor()
        paths = [{"North": False}, {"East": True}, {"South": True}, {"West": True}]
